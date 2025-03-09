(() => {
  let controller = new AbortController(),
    debounceTimer;

  const searchContainer = document.querySelector('.search-container'),
    searchForm = document.querySelector('.search-form'),
    searchInput = document.querySelector('.search-form__input'),
    suggestionsList = document.querySelector('.suggestions'),
    rootElement = document.querySelector('#root');

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

  function removeChildren(element) {
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }

    element.textContent = '';
  }

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

    if (suggestions.length === 0) {
      const suggestionsError = document.createElement('p');

      suggestionsError.textContent = `هیچ گونه پیشنهادی با عنوان "${query}" یافت نشد.`;
      suggestionsError.classList.add('suggestions__error');
      suggestionsList.appendChild(suggestionsError);
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
      !!suggestionsList.querySelector('.suggestions__loading-spinner') || false;

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

    const hasActiveSuggestion =
        searchContainer.classList.contains('showing-results') &&
        suggestionsList.querySelector('.suggestions__item.active'),
      selectedSuggestion = hasActiveSuggestion
        ? suggestionsList.querySelector('.suggestions__item.active').dataset
            .content
        : searchInput.value;
  }

  const ROUTER = {
    '/': {
      onRoute() {},
      cleanUp() {},
    },
    '/search:q': {
      async onRoute() {
        const results = await fetchData(
          `https://engine2.vajehyab.com/search?q=${__CURRENT_WORD__}`
        );

        if (Object.prototype.toString.call(results) !== '[object Object]') {
          return;
        }

        const wordMeanings = results.wordbox.sections;

        console.log(wordMeanings[0].description);
      },
      clenaUp() {},
    },
    404: {
      onRoute() {},
      cleanUp() {},
    },
  };

  function getRoute() {
    const { pathname, search: searchParams } = window.location;

    if (pathname === '/') {
      return '/';
    }

    const isSearching =
      (pathname.startsWith('/search/') &&
        new URLSearchParams(searchParams).get('q')) ||
      pathname.startsWith('/word/');

    if (isSearching) {
      return '/search:q';
    }

    return 404;
  }

  async function navigate(ev) {
    if (
      !(
        Object.prototype.toString.call(ev) === '[object Event]' &&
        ev.type === 'load'
      )
    ) {
      const routeHTML = await fetchData(window.location.href, {
          mode: 'same-origin',
          keepalive: true,
          priority: 'high',
        }),
        parsedHTML = new DOMParser()
          .parseFromString(routeHTML, 'text/html')
          .querySelector('#root').children;

      removeChildren(rootElement);
      rootElement.append(...parsedHTML);
    }

    const currentRoute = getRoute();
    ROUTER[currentRoute].onRoute();
  }

  function handleDocumentClick({ target: targetElement }) {
    if (
      !targetElement.matches('a.suggestions__link[href][data-spa-link="true"]')
    ) {
      return;
    }

    history.pushState(null, null, targetElement.href);
    __CURRENT_WORD__ = targetElement.parentElement.dataset.content;
    navigate();
  }

  searchInput.addEventListener('blur', handleBlur);
  searchInput.addEventListener('focus', handleFocus);
  searchInput.addEventListener('input', handleInput);
  searchForm.addEventListener('submit', handleSubmit);
  document.addEventListener('keydown', handleKeyDown);
  document.addEventListener('mousedown', handleDocumentClick);
  window.addEventListener('popstate', navigate);
  window.addEventListener('load', navigate);
})();
