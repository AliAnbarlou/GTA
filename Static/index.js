const HTML_ELEMENT = document.documentElement,
  themeToggler = document.querySelector(".header__theme-toggler");

HTML_ELEMENT.dataset.theme =
  JSON.parse(localStorage.getItem("current-theme")) || "light";

function handleClick(ev) {
  ev.stopPropagation();

  const currentTheme =
    JSON.parse(localStorage.getItem("current-theme")) ||
    HTML_ELEMENT.dataset.theme;

  HTML_ELEMENT.dataset.theme = currentTheme === "light" ? "dark" : "light";

  localStorage.setItem(
    "current-theme",
    JSON.stringify(HTML_ELEMENT.dataset.theme)
  );
}

themeToggler.addEventListener("click", handleClick);
