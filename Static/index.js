(() => {
  const rootElement = document.querySelector('#root');

  async function fetchData(url = '.', options) {
    try {
      const response = await fetch(url, options);

      if (!response.ok) {
        return null;
      }

      const contentType = response.headers.get('Content-Type');

      if (contentType.startsWith('application/json')) {
        return await response.json();
      }

      if (contentType.startsWith('text/')) {
        return await response.text();
      }

      if (contentType.startsWith('image/')) {
        return await response.blob();
      }

      if (contentType.startsWith('application/octet-stream')) {
        return await response.arrayBuffer();
      }

      return await response.text();
    } catch (error) {
      return null;
    }
  }

  function parseStringToHtml(data) {
    if (typeof data !== 'string') {
      return { parsedRoute: [], hasError: true };
    }

    const parsedDocument = new DOMParser().parseFromString(data, 'text/html'),
      parsedDocumentRootElement = parsedDocument.querySelector('#root');

    if (!parsedDocumentRootElement) {
      console.log('Shit');

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

    element.textContent = '';
  }

  const router = {
    '/': {
      regexPattern: /^\/$/,
    },
    '/search': {
      regexPattern: /^\/search\/?$/,
      HANDLE_TEXTAREA({ target: textAreaElement }) {
        textAreaElement.style.height = 'auto';
        textAreaElement.style.height = `${textAreaElement.scrollHeight}px`;
      },
      onRouteLoad() {
        __CURRENT_WORD__ = new URLSearchParams(location.search).get('q');

        const textAreas = document.querySelectorAll('.textarea');

        textAreas.forEach((textArea) => {
          textArea.addEventListener('input', this.HANDLE_TEXTAREA);
        });
      },
    },
    404: {},
    onLoad() {
      let controller = new AbortController(),
        debounceTimer;

      const searchContainer = document.querySelector('.search-container'),
        searchForm = document.querySelector('.search-form'),
        searchInput = document.querySelector('.search-form__input'),
        suggestionsList = document.querySelector('.suggestions');

      async function fetchSuggestions(query) {
        controller.abort();
        controller = new AbortController();

        try {
          const response = await fetch(`/word/api/${query}`, {
            signal: controller.signal,
          });

          if (!response.ok) {
            throw new Error('خطا در دریافت داده');
          }

          return [query, (await response.json()).hits] || [query, []];
        } catch (error) {
          return [query, []];
        }
      }

      function renderSuggestions([query, suggestions]) {
        removeChildren(suggestionsList);

        suggestions = suggestions.filter((suggestion) =>
          /^(?:[\u0600-\u06FF\s]+|[a-zA-Z\s]+)$/.test(suggestion.title)
        );

        if (suggestions.length === 0) {
          const suggestionsError = document.createElement('p');

          suggestionsError.textContent = `هیچ گونه پیشنهادی با عنوان "${query}" یافت نشد.`;
          suggestionsError.classList.add('suggestions__error');
          suggestionsList.appendChild(suggestionsError);
          return;
        }

        suggestions.unshift({ title: query });

        const fragment = document.createDocumentFragment();

        suggestions.forEach(({ title }) => {
          const suggestionItem = document.createElement('li'),
            suggestionLink = document.createElement('a');

          suggestionLink.textContent = title;
          suggestionItem.dataset.content = title;
          suggestionLink.dataset.spaLink = true;
          suggestionLink.href = `/search/?q=${title}`;
          suggestionLink.classList.add('suggestions__link');
          suggestionItem.classList.add('suggestions__item');
          suggestionItem.appendChild(suggestionLink);
          fragment.appendChild(suggestionItem);
        });

        suggestionsList.appendChild(fragment);
      }

      function handleBlur() {
        searchContainer.classList.remove('showing-results');
      }

      function handleFocus() {
        if (suggestionsList.childElementCount > 0) {
          searchContainer.classList.add('showing-results');
        }
      }

      function handleInput() {
        clearTimeout(debounceTimer);

        const inputValue = searchInput.value.trim();

        if (inputValue.length <= 1) {
          removeChildren(suggestionsList);
          searchContainer.classList.remove('showing-results');
          return;
        }

        const hasLoadingSppiner =
          !!suggestionsList.querySelector('.suggestions__loading-spinner') ||
          false;

        if (!hasLoadingSppiner) {
          removeChildren(suggestionsList);
          const loadingSppiner = document.createElement('span');

          loadingSppiner.classList.add('suggestions__loading-spinner');
          suggestionsList.appendChild(loadingSppiner);
        }

        searchContainer.classList.add('showing-results');

        debounceTimer = setTimeout(async () => {
          const suggestions = await fetchSuggestions(inputValue);
          renderSuggestions(suggestions);
        }, 850);
      }

      function handleKeyDown({ key: pressedKeyboardKey }) {
        if (
          pressedKeyboardKey !== 'ArrowUp' &&
          pressedKeyboardKey !== 'ArrowDown'
        ) {
          return;
        }

        const hasSuggestionsItem =
          !!suggestionsList.querySelector('.suggestions__item') || false;

        if (!hasSuggestionsItem) {
          return;
        }

        const activeSuggestion = suggestionsList.querySelector(
          '.suggestions__item.active'
        );

        if (!activeSuggestion) {
          suggestionsList.firstChild.classList.add('active');
          return;
        }

        activeSuggestion.classList.remove('active');

        let nextActiveSuggestion;

        if (pressedKeyboardKey === 'ArrowUp') {
          nextActiveSuggestion =
            activeSuggestion === suggestionsList.firstElementChild
              ? suggestionsList.lastElementChild
              : activeSuggestion.previousElementSibling;
        }

        if (pressedKeyboardKey === 'ArrowDown') {
          nextActiveSuggestion =
            activeSuggestion === suggestionsList.lastElementChild
              ? suggestionsList.firstElementChild
              : activeSuggestion.nextElementSibling;
        }

        nextActiveSuggestion.classList.add('active');
        searchInput.value = nextActiveSuggestion.dataset.content;
      }

      async function handleSubmit(ev) {
        ev.preventDefault();

        const selectedSuggestion = searchInput.value;
        navigate(`/search/?q=${selectedSuggestion}`);
        searchContainer.classList.remove('showing-results');
      }

      searchInput.addEventListener('blur', handleBlur);
      searchInput.addEventListener('focus', handleFocus);
      searchInput.addEventListener('input', handleInput);
      searchForm.addEventListener('submit', handleSubmit);
      document.addEventListener('keydown', handleKeyDown);
    },
  };

  const routes = Object.keys(router).filter(
    (route) => route !== 'onLoad' && route !== '404'
  );

  function handleRoutes() {
    const matchedRoute =
      router[
        routes.find((route) =>
          router[route].regexPattern.test(location.pathname)
        )
      ] || router[404];

    if (typeof matchedRoute === 'function') {
      matchedRoute();
      return;
    }

    if (typeof matchedRoute.onRouteLoad === 'function') {
      matchedRoute.onRouteLoad();
      return;
    }
  }

  async function navigate(url) {
    const { parsedRoute, hasError } = parseStringToHtml(await fetchData(url));

    if (hasError && url === '/404') {
      return;
    }

    if (hasError) {
      navigate('/404');
      return;
    }

    removeChildren(rootElement);
    rootElement.append(...parsedRoute);
    history.pushState(null, '', url);
    handleRoutes();
  }

  function handleMouseDown({ target: targetElement }) {
    if (targetElement.matches('a[data-spa-link="true"][href]')) {
      navigate(targetElement.href);
      return;
    }

    if (targetElement.matches('.question__answers-toggler')) {
      const closestQuestionAnswers = targetElement.nextElementSibling;

      if (!closestQuestionAnswers.matches('.question__answers')) {
        return;
      }

      closestQuestionAnswers.classList.toggle('show');
    }
  }

  router.onLoad();
  handleRoutes();

  window.addEventListener('popstate', handleRoutes);
  document.addEventListener('mousedown', handleMouseDown);
})();
