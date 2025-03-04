(() => {
  const searchContainer = document.querySelector('.search-container');
  const searchInput = document.querySelector('.search-form__input');
  const suggestionsList = document.querySelector('.suggestions');
  let controller = new AbortController();
  let debounceTimer;

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
      const response = await fetch(
        `https://engine2.vajehyab.com/suggestion?q=${encodeURIComponent(
          query
        )}`,
        { signal: controller.signal }
      );

      if (!response.ok) {
        throw new Error('خطا در دریافت داده');
      }

      return (await response.json()).hits || [];
    } catch (error) {
      if (error.name !== 'AbortError') {
        console.error('Request failed:', error);
      }

      return [];
    }
  }

  function renderSuggestions(suggestions) {
    searchContainer.classList.add('showing-results');

    removeChildren(suggestionsList);

    const fragment = document.createDocumentFragment();

    suggestions.forEach(({ title }) => {
      const item = document.createElement('li');
      item.classList.add('suggestions__item');
      item.textContent = title;
      fragment.appendChild(item);
    });

    suggestionsList.appendChild(fragment);
  }

  function handleKeydown(ev) {
    const pressedKeyboardKey = ev.key;

    if (
      pressedKeyboardKey !== 'ArrowUp' &&
      pressedKeyboardKey !== 'ArrowDown'
    ) {
      return;
    }

    const suggestionListChildren = suggestionsList.children,
      suggestionsListLength = suggestionListChildren.length;

    if (suggestionsListLength === 0) {
      return;
    }

    const currentActiveSuggestions = suggestionsList.querySelector(
        'suggestions__item.active'
      ),
      isLastChildren =
        !currentActiveSuggestions ||
        currentActiveSuggestions ===
          suggestionListChildren.item(suggestionsListLength - 1);

    currentActiveSuggestions.classList.remove('active');

    (isLastChildren
      ? suggestionsList.children.item(0)
      : currentActiveSuggestions.nextElementSibling
    ).classList.add('active');
  }

  function handleInput() {
    clearTimeout(debounceTimer);

    const inputValue = searchInput.value.trim();

    if (inputValue.length <= 1) {
      removeChildren(suggestionsList);
      searchContainer.classList.remove('showing-results');
      return;
    }

    const loadingSppiner = document.createElement('span');
    loadingSppiner.classList.add('suggestions__loading-spinner');
    suggestionsList.appendChild(loadingSppiner);

    searchContainer.classList.add('showing-results');

    debounceTimer = setTimeout(async () => {
      const suggestions = await fetchSuggestions(inputValue);
      renderSuggestions(suggestions);
    }, 850);
  }

  function handleBlur() {
    searchContainer.classList.remove('showing-results');
  }

  function handleFocus() {
    if (suggestionsList.children.length > 0) {
      searchContainer.classList.add('showing-results');
    }

    document.addEventListener('keydown', handleKeydown);
  }

  searchInput.addEventListener('input', handleInput);
})();
