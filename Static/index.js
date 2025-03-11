(() => {
  let currentRoute = '';

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

  const router = {
    type: 'layout',
    onLoad() {
      const themeToggler = document.querySelector('.header__theme-toggler');
    },
    children: [
      {
        type: 'layout',
        onLoad() {},
        children: [],
      },
      {
        type: 'layout',
        onLoad() {},
        children: [],
      },
    ],
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
