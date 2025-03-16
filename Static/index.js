// (() => {
//   function removeChildren(element) {
//     while (element.firstChild) {
//       element.removeChild(element.firstChild);
//     }

//     element.textContent = "";
//   }

// async function fetchData(url = ".", options) {
//   try {
//     const response = await fetch(url, options);

//     if (!response.ok) {
//       return null;
//     }

//     const contentType = response.headers.get("Content-Type");

//     if (contentType.startsWith("application/json")) {
//       return await response.json();
//     }

//     if (contentType.startsWith("text/")) {
//       return await response.text();
//     }

//     if (contentType.startsWith("image/")) {
//       return await response.blob();
//     }

//     if (contentType.startsWith("application/octet-stream")) {
//       return await response.arrayBuffer();
//     }

//     return await response.text();
//   } catch (error) {
//     return null;
//   }
// }

//   function onSearchLayoutLoad() {
//   let controller = new AbortController(),
//     debounceTimer;

//   const searchContainer = document.querySelector(".search-container"),
//     searchForm = document.querySelector(".search-form"),
//     searchInput = document.querySelector(".search-form__input"),
//     suggestionsList = document.querySelector(".suggestions");

//   async function fetchSuggestions(query) {
//     controller.abort();

//     const data = await fetchData(
//       `https://engine2.vajehyab.com/suggestion?q=${query}`
//     );

//     if (Object.prototype.toString.call(data) !== "[object Object]") {
//       throw new Error("خطا در دریافت داده");
//     }

//     return [query, data.hits] || [query, []];
//   }

//   function renderSuggestions([query, suggestions]) {
//     removeChildren(suggestionsList);

//     suggestions = suggestions.filter((suggestion) =>
//       /^(?:[\u0600-\u06FF\s]+|[a-zA-Z\s]+)$/.test(suggestion.title)
//     );

//     if (suggestions.length === 0) {
//       const suggestionsError = document.createElement("p");

//       suggestionsError.textContent = `هیچ گونه پیشنهادی با عنوان "${query}" یافت نشد.`;
//       suggestionsError.classList.add("suggestions__error");
//       suggestionsList.appendChild(suggestionsError);
//       return;
//     }

//     suggestions.unshift({ title: query });

//     const fragment = document.createDocumentFragment();

//     suggestions.forEach(({ title }) => {
//       const suggestionItem = document.createElement("li"),
//         suggestionLink = document.createElement("a");

//       suggestionLink.textContent = title;
//       suggestionItem.dataset.content = title;
//       suggestionLink.dataset.spaLink = true;
//       suggestionLink.href = `/search/?q=${title}`;
//       suggestionLink.classList.add("suggestions__link");
//       suggestionItem.classList.add("suggestions__item");
//       suggestionItem.appendChild(suggestionLink);
//       fragment.appendChild(suggestionItem);
//     });

//     suggestionsList.append(fragment);
//   }

//   function handleBlur() {
//     setTimeout(() => {
//       searchContainer.classList.remove("showing-results");
//     }, 0);
//   }

//   function handleFocus() {
//     if (suggestionsList.childElementCount > 0) {
//       searchContainer.classList.add("showing-results");
//     }
//   }

//   function handleInput() {
//     const inputValue = searchInput.value;

//     if (inputValue.length <= 1) {
//       removeChildren(suggestionsList);
//       searchContainer.classList.remove("showing-results");
//       return;
//     }

//     const hasLoadingSppiner =
//       !!suggestionsList.querySelector(".suggestions__loading-spinner") ||
//       false;

//     if (!hasLoadingSppiner) {
//       removeChildren(suggestionsList);
//       const loadingSppiner = document.createElement("span");

//       loadingSppiner.classList.add("suggestions__loading-spinner");
//       suggestionsList.appendChild(loadingSppiner);
//     }

//     searchContainer.classList.add("showing-results");

//     debounceTimer = setTimeout(async () => {
//       const suggestions = await fetchSuggestions(inputValue);
//       renderSuggestions(suggestions);
//     }, 600);
//   }

//   function handleKeyDown({ key: pressedKeyboardKey }) {
//     if (
//       pressedKeyboardKey !== "ArrowUp" &&
//       pressedKeyboardKey !== "ArrowDown"
//     ) {
//       return;
//     }

//     const hasSuggestionsItem =
//       !!suggestionsList.querySelector(".suggestions__item") || false;

//     if (!hasSuggestionsItem) {
//       return;
//     }

//     const activeSuggestion = suggestionsList.querySelector(
//       ".suggestions__item.active"
//     );

//     if (!activeSuggestion) {
//       suggestionsList.firstChild.classList.add("active");
//       return;
//     }

//     activeSuggestion.classList.remove("active");

//     let nextActiveSuggestion;

//     if (pressedKeyboardKey === "ArrowUp") {
//       nextActiveSuggestion =
//         activeSuggestion === suggestionsList.firstElementChild
//           ? suggestionsList.lastElementChild
//           : activeSuggestion.previousElementSibling;
//     }

//     if (pressedKeyboardKey === "ArrowDown") {
//       nextActiveSuggestion =
//         activeSuggestion === suggestionsList.lastElementChild
//           ? suggestionsList.firstElementChild
//           : activeSuggestion.nextElementSibling;
//     }

//     nextActiveSuggestion.classList.add("active");
//     searchInput.value = nextActiveSuggestion.dataset.content;
//   }

//   async function handleSubmit(ev) {
//     ev.preventDefault();

//     const selectedSuggestion = searchInput.value;
//     // navigate(`/search/?q=${selectedSuggestion}`);
//     searchContainer.classList.remove("showing-results");
//   }

//   searchInput.addEventListener("blur", handleBlur);
//   searchInput.addEventListener("focus", handleFocus);
//   searchInput.addEventListener("input", handleInput);
//   searchForm.addEventListener("submit", handleSubmit);
//   document.addEventListener("keydown", handleKeyDown);
// }

//   function setPaths(router) {
//     if (router.type === 'route') {
//       return [router.path];
//     }

//     if (router.type === 'layout') {
//       router.paths = router.children.flatMap((child) => {
//         return setPaths(child);
//       });
//     }

//     if (router.type === 'root-layout') {
//       router.children.forEach((child) => {
//         setPaths(child);
//       });
//     }
//   }

//   const HTML_ELEMENT = document.documentElement;

//   const router = {
//     type: "root-layout",
//     onLoad() {
// const themeToggler = document.querySelector(".header__theme-toggler");

// HTML_ELEMENT.dataset.theme =
//   JSON.parse(localStorage.getItem("current-theme")) || "light";

// function handleClick(ev) {
//   ev.stopPropagation();

//   const currentTheme =
//     JSON.parse(localStorage.getItem("current-theme")) ||
//     HTML_ELEMENT.dataset.theme;

//   HTML_ELEMENT.dataset.theme =
//     currentTheme === "light" ? "dark" : "light";

//   localStorage.setItem(
//     "current-theme",
//     JSON.stringify(HTML_ELEMENT.dataset.theme)
//   );
// }

// themeToggler.addEventListener("click", handleClick);
//     },
//     children: [
//       {
//         onLoad: onSearchLayoutLoad,
//         type: "layout",
//         children: [
//           {
//             type: "route",
//             path: /^\/$/,
//             rootElementCssSelector: '.root',
//           },
//           {
//             type: "route",
//             path: /^\/search\/$/,
//             rootElementCssSelector: '.root',
//           },
//         ]
//       },
//     ]
//   };

//   setPaths(router);

//   const ERROR_ROUTE = {
//     type: 'route',
//     path: /^\/404\/$/,
//     onLoad() {},
//   };

//   let currentRoute = "";

//   function getRouteDetails(router, consideredRoute) {
//     if (router.type === 'route' && router.path.test(location.pathname)) {
//       return router;
//     }

//     if (router.type === 'layout' && router.paths.some((path) => path.test(location.pathname))) {
//       for (let child of router.children) {
//         const result = getRouteDetails(child, consideredRoute);

//         if (result !== ERROR_ROUTE) {
//           return result;
//         }
//       }
//     }

//     if (router.type === 'root-layout') {
//       for (let child of router.children) {
//         const result = getRouteDetails(child, consideredRoute);

//         if (result !== ERROR_ROUTE) {
//           return result;
//         }
//       }
//     }

//     return ERROR_ROUTE;
//   }

// function parseStringToHtml(data) {
//   if (typeof data !== "string") {
//     return { parsedRoute: [], hasError: true };
//   }

//   const parsedDocument = new DOMParser().parseFromString(data, "text/html"),
//     parsedDocumentRootElement = parsedDocument.querySelector(".root");

//   if (!parsedDocumentRootElement) {
//     console.log("Shit");

//     return { parsedRoute: [], hasError: true };
//   }

//   return {
//     parsedRoute: Array.from(parsedDocumentRootElement.children),
//     hasError: false,
//   };
// }

//   function handleRoute() {
//     const layoutCallbacks = [];

//     function collectOnLoadCallbacks(router) {
//       if (
//         router.type === 'root-layout' ||
//         (router.type === 'layout' && router.paths.some(path => path.test(location.pathname)))
//       ) {
//         layoutCallbacks.push(router.onLoad);
//         router.children.forEach(collectOnLoadCallbacks);
//       } else if (router.type === 'route' && router.path.test(location.pathname)) {
//         if (typeof router.onLoad === 'function') {
//           layoutCallbacks.push(router.onLoad);
//         }
//       }
//     }

//     collectOnLoadCallbacks(router);

//     layoutCallbacks.forEach(callback => {
//       if (typeof callback === 'function') {
//         callback();
//       }
//     });
//   }

//   async function navigate(url) {
//     history.pushState(null, '', url);
//     console.log(getRouteDetails(router));
//   }

//   function handleDocumentClick({ target: targetElement }) {
//     if (
//       targetElement.matches('a[href][data-spa-link="true"]') &&
//       targetElement.origin === window.location.origin
//     ) {
//       navigate(targetElement.href);
//     }
//   }

//   handleRoute();

//   document.addEventListener("mousedown", handleDocumentClick);
// })();

(() => {
  const layouts = [
    {
      name: "RootLayout",
      onLoad() {
        const HTML_ELEMENT = document.documentElement,
          themeToggler = document.querySelector(".header__theme-toggler");

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
      rootElement: "#__ROOT",
    },
    {
      name: "SearchLayout",
      onLoad() {
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

          if (suggestions.length === 0) {
            const suggestionsError = document.createElement("p");

            suggestionsError.textContent = `هیچ گونه پیشنهادی با عنوان "${query}" یافت نشد.`;
            suggestionsError.classList.add("suggestions__error");
            suggestionsList.appendChild(suggestionsError);
            return;
          }

          suggestions.unshift({ title: query });

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
          console.log("hey");
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
            // return;
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
      },
      parentLayout: "RootLayout",
      rootElement: "#__SEARCH",
    },
    {
      name: "UserBase",
      onLoad() {},
      parentLayout: "RootLayout",
      rootElement: "#__USER_BASE",
    },
  ];

  const routes = [
    {
      path: "/",
      layout: "SearchLayout",
      onLoad() {},
    },
    {
      path: "/search/",
      layout: "SearchLayout",
      onLoad() {},
    },
    {
      path: "/profile/",
      layout: "UserBase",
      onLoad() {},
    },
  ];

  const ROUTE_404 = {
    type: "error",
    layout: "RootLayout",
    onLoad() {},
  };

  function removeChildren(element) {
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }
  }

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

  function parseStringToHtml(data, rootSelector) {
    if (typeof data !== "string") {
      return { parsedRoute: [], hasError: true };
    }

    const parsedDocument = new DOMParser().parseFromString(data, "text/html"),
      parsedDocumentRootElement = parsedDocument.querySelector(rootSelector);

    if (!parsedDocumentRootElement) {
      console.log("Shit");

      return { parsedRoute: [], hasError: true };
    }

    return {
      parsedRoute: Array.from(parsedDocumentRootElement.children),
      hasError: false,
    };
  }

  function findCommonParent(...considerdLayouts) {
    function getParentChain(considerdLayout) {
      const parentChain = [];

      do {
        parentChain.push(considerdLayout.name);

        if (considerdLayout.parentLayout) {
          parentChain.push(considerdLayout.parentLayout);
        }

        considerdLayout = layouts.find(
          (layout) => layout.name === considerdLayout.parentLayout
        );
      } while (considerdLayout.parentLayout);

      return parentChain.length === 0 ? null : parentChain;
    }

    function getCommonParent(accumulator, currentParentChain) {
      return accumulator.filter((element) =>
        currentParentChain.includes(element)
      );
    }

    const convertedToParentChain = considerdLayouts.map(getParentChain);

    return convertedToParentChain.reduce(getCommonParent)[0];
  }

  function findRoute(url) {
    const matchedRoute =
      routes.find((route) => route.path === url) || ROUTE_404;

    const matchedLayout = layouts.find(
      (layout) => layout.name === matchedRoute.layout
    );

    return [matchedRoute, matchedLayout];
  }

  function callOnLoadCallbacks([matchedRoute, matchedLayout]) {
    const onLoadCallbacks = [];

    if (matchedRoute.onLoad instanceof Function) {
      onLoadCallbacks.push(matchedRoute.onLoad);
    }

    do {
      if (matchedLayout.onLoad instanceof Function) {
        onLoadCallbacks.push(matchedLayout.onLoad);
      }

      matchedLayout = layouts.find(
        (layout) => layout.name === matchedLayout.parentLayout
      );
    } while (matchedLayout.parentLayout);

    if (matchedLayout.onLoad instanceof Function) {
      onLoadCallbacks.push(matchedLayout.onLoad);
    }

    onLoadCallbacks.reverse().forEach((onLoadCallback) => {
      onLoadCallback();
    });
  }

  function handleRoute() {
    callOnLoadCallbacks(findRoute(location.pathname));
  }

  async function render() {
    const {
      previousRouteDetails: [prevMatchedRoute, prevMatchedLayout],
      newRouteDetails: [newMatchedRoute, newMatchedLayout],
    } = history.state;

    if (newMatchedRoute.type === "error") {
      return;
    }

    const sharedLayout = findCommonParent(prevMatchedLayout, newMatchedLayout),
      sharedRootElement = document.querySelector(sharedLayout.rootElement);

    const { parsedRoute, hasError } = parseStringToHtml(
      await fetchData(location.href),
      sharedLayout.rootElement
    );

    if (hasError) {
      await navigate("/404");
      return;
    }

    sharedRootElement.append(...parsedRoute);
  }

  async function navigate(url = "/") {
    const absoluteUrl = new URL(url, window.location.origin),
      newRouteDetails = findRoute(absoluteUrl.pathname),
      previousRouteDetails = findRoute(location.pathname);

    history.pushState(
      {
        previousRouteDetails,
        newRouteDetails,
      },
      "",
      url
    );

    await render();
    callOnLoadCallbacks(newRouteDetails);
  }

  function handleDocumentClick(ev) {
    const targetElement = ev.target;

    ev.preventDefault();

    if (
      targetElement.matches('a[href][data-spa-link="true"]') &&
      targetElement.href.startsWith(window.location.origin)
    ) {
      ev.preventDefault();
      navigate(targetElement.href);
    }
  }

  window.addEventListener("popstate", handleRoute);
  document.addEventListener("DOMContentLoaded", handleRoute);
  document.addEventListener("mousedown", handleDocumentClick);
})();
