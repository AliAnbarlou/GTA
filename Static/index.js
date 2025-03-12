(() => {
  const HTML_ELEMENT = document.documentElement;
  let currentRoute = "";

  async function fetchData(url = ".", options) {
    try {
      const response = await fetch(url, options);

      if (!response.ok) {
        return null;
      }

      const contentType = response.headers.get("Content-Type");

      if (contentType.startsWith("application/json")) {
        return await response.json();
      }

      if (contentType.startsWith("text/")) {
        return await response.text();
      }

      if (contentType.startsWith("image/")) {
        return await response.blob();
      }

      if (contentType.startsWith("application/octet-stream")) {
        return await response.arrayBuffer();
      }

      return await response.text();
    } catch (error) {
      return null;
    }
  }

  function parseStringToHtml(data) {
    if (typeof data !== "string") {
      return { parsedRoute: [], hasError: true };
    }

    const parsedDocument = new DOMParser().parseFromString(data, "text/html"),
      parsedDocumentRootElement = parsedDocument.querySelector("#root");

    if (!parsedDocumentRootElement) {
      console.log("Shit");

      return { parsedRoute: [], hasError: true };
    }

    return {
      parsedRoute: Array.from(parsedDocumentRootElement.children),
      hasError: false,
    };
  }

  function removeChildren(element) {
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }

    element.textContent = "";
  }

  // const router = {

  //   '/': {
  //     regexPattern: /^\/$/,
  //     get parentRoot() {
  //       return document.querySelector('#root');
  //     },
  //     onParentRootLoad() {}
  //   },
  //   '/search': {
  //     regexPattern: /^\/search\/?$/,
  //     get parentRoot() {
  //       return document.querySelector('#root');
  //     },
  //     HANDLE_TEXTAREA({ target: textAreaElement }) {
  //       textAreaElement.style.height = 'auto';
  //       textAreaElement.style.height = `${textAreaElement.scrollHeight}px`;
  //     },
  //     onRouteLoad() {
  //       __CURRENT_WORD__ = new URLSearchParams(location.search).get('q');

  //       const textAreas = document.querySelectorAll('.textarea');

  //       textAreas.forEach((textArea) => {
  //         textArea.addEventListener('input', this.HANDLE_TEXTAREA);
  //       });
  //     },
  //   },
  //   404: {},
  //   onRootLayoutLoad() {

  //   },
  // };

  function onSearchLoad() {
    let controller = new AbortController(),
      debounceTimer;

    const searchContainer = document.querySelector(".search-container"),
      searchForm = document.querySelector(".search-form"),
      searchInput = document.querySelector(".search-form__input"),
      suggestionsList = document.querySelector(".suggestions");

    async function fetchSuggestions(query) {
      controller.abort();

      const data = await fetchData(
        `https://engine2.vajehyab.com/suggestion?q=${query}`
      );

      if (Object.prototype.toString.call(data) !== "[object Object]") {
        throw new Error("خطا در دریافت داده");
      }

      return [query, data.hits] || [query, []];
    }

    function renderSuggestions([query, suggestions]) {
      removeChildren(suggestionsList);

      suggestions = suggestions.filter((suggestion) =>
        /^(?:[\u0600-\u06FF\s]+|[a-zA-Z\s]+)$/.test(suggestion.title)
      );

      console.log(suggestions);

      if (suggestions.length === 0) {
        const suggestionsError = document.createElement("p");

        suggestionsError.textContent = `هیچ گونه پیشنهادی با عنوان "${query}" یافت نشد.`;
        suggestionsError.classList.add("suggestions__error");
        suggestionsList.appendChild(suggestionsError);
        return;
      }

      const fragment = document.createDocumentFragment();

      suggestions.forEach(({ title }) => {
        const suggestionItem = document.createElement("li"),
          suggestionLink = document.createElement("a");

        suggestionLink.textContent = title;
        suggestionItem.dataset.content = title;
        suggestionLink.dataset.spaLink = true;
        suggestionLink.href = `/search/?q=${title}`;
        suggestionLink.classList.add("suggestions__link");
        suggestionItem.classList.add("suggestions__item");
        suggestionItem.appendChild(suggestionLink);
        fragment.appendChild(suggestionItem);
      });

      suggestionsList.append(fragment);
    }

    function handleBlur() {
      setTimeout(() => {
        searchContainer.classList.remove("showing-results");
      }, 0);
    }

    function handleFocus() {
      if (suggestionsList.childElementCount > 0) {
        searchContainer.classList.add("showing-results");
      }
    }

    function handleInput() {
      const inputValue = searchInput.value;

      if (inputValue.length <= 1) {
        removeChildren(suggestionsList);
        searchContainer.classList.remove("showing-results");
        return;
      }

      const hasLoadingSppiner =
        !!suggestionsList.querySelector(".suggestions__loading-spinner") ||
        false;

      if (!hasLoadingSppiner) {
        removeChildren(suggestionsList);
        const loadingSppiner = document.createElement("span");

        loadingSppiner.classList.add("suggestions__loading-spinner");
        suggestionsList.appendChild(loadingSppiner);
      }

      searchContainer.classList.add("showing-results");

      debounceTimer = setTimeout(async () => {
        const suggestions = await fetchSuggestions(inputValue);
        renderSuggestions(suggestions);
      }, 600);
    }

    function handleKeyDown({ key: pressedKeyboardKey }) {
      if (
        pressedKeyboardKey !== "ArrowUp" &&
        pressedKeyboardKey !== "ArrowDown"
      ) {
        return;
      }

      const hasSuggestionsItem =
        !!suggestionsList.querySelector(".suggestions__item") || false;

      if (!hasSuggestionsItem) {
        return;
      }

      const activeSuggestion = suggestionsList.querySelector(
        ".suggestions__item.active"
      );

      if (!activeSuggestion) {
        suggestionsList.firstChild.classList.add("active");
        return;
      }

      activeSuggestion.classList.remove("active");

      let nextActiveSuggestion;

      if (pressedKeyboardKey === "ArrowUp") {
        nextActiveSuggestion =
          activeSuggestion === suggestionsList.firstElementChild
            ? suggestionsList.lastElementChild
            : activeSuggestion.previousElementSibling;
      }

      if (pressedKeyboardKey === "ArrowDown") {
        nextActiveSuggestion =
          activeSuggestion === suggestionsList.lastElementChild
            ? suggestionsList.firstElementChild
            : activeSuggestion.nextElementSibling;
      }

      nextActiveSuggestion.classList.add("active");
      searchInput.value = nextActiveSuggestion.dataset.content;
    }

    async function handleSubmit(ev) {
      ev.preventDefault();

      const selectedSuggestion = searchInput.value;
      // navigate(`/search/?q=${selectedSuggestion}`);
      searchContainer.classList.remove("showing-results");
    }

    searchInput.addEventListener("blur", handleBlur);
    searchInput.addEventListener("focus", handleFocus);
    searchInput.addEventListener("input", handleInput);
    searchForm.addEventListener("submit", handleSubmit);
    document.addEventListener("keydown", handleKeyDown);
  }

  const router = {
    type: "layout",
    path: "/",
    rootElement: document,
    onLoad() {
      const themeToggler = document.querySelector(".header__theme-toggler");

      HTML_ELEMENT.dataset.theme =
        JSON.parse(localStorage.getItem("current-theme")) || "light";

      function handleClick(ev) {
        ev.stopPropagation();

        const currentTheme =
          JSON.parse(localStorage.getItem("current-theme")) ||
          HTML_ELEMENT.dataset.theme;

        HTML_ELEMENT.dataset.theme =
          currentTheme === "light" ? "dark" : "light";

        localStorage.setItem(
          "current-theme",
          JSON.stringify(HTML_ELEMENT.dataset.theme)
        );
      }

      themeToggler.addEventListener("click", handleClick);
    },
    children: [
      {
        type: "route",
        path: "/",
        onLoad: onSearchLoad,
      },
      {
        type: "layout",
        get rootElement() {
          return document.querySelector(".root");
        },
        path: "/search/",
        onLoad() {
          onSearchLoad();
        },
        children: [],
      },
      {
        type: "layout",
        path: "/profile/",
        onLoad() {},
        children: [],
      },
    ],
  };

  function handleRoute() {
    const layoutCallbacks = [];

    function collectOnLoadCallbacks(router) {
      if (
        router.type === "route" &&
        location.pathname.startsWith(router.path)
      ) {
        if (typeof router.onLoad === "function") {
          layoutCallbacks.push(router.onLoad);
        }

        return { FOUNDED_ROUTE: true };
      }

      if (
        router.type === "layout" &&
        location.pathname.startsWith(router.path)
      ) {
        if (typeof router.onLoad === "function") {
          layoutCallbacks.push(router.onLoad);
        }

        for (const slug of router.children) {
          collectOnLoadCallbacks(slug);
        }
      }
    }

    collectOnLoadCallbacks(router);

    layoutCallbacks.forEach((callback) => {
      callback();
    });
  }

  function getCurrentRouteDetails(router) {
    for (const key in router) {
      const route = router[key];

      if (route.path === location.pathname) {
        return route;
      }

      const found = getCurrentRouteDetails(router.children);

      if (found) {
        return found;
      }
    }

    return {
      type: "route",
      path: "/404",
      children: [],
    };
  }

  async function navigate(url) {
    const parsedDocument = await fetchData(url);
  }

  function handleDocumentClick({ target: targetElement }) {
    if (
      targetElement.matches('a[href][data-spa-link="true"]') &&
      targetElement.origin === window.location.origin
    ) {
      
    }
  }

  handleRoute();

  document.addEventListener("mousedown", handleDocumentClick);
})();
