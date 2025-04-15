const HTML_ELEMENT = document.documentElement,
  themeToggler = document.querySelector(".header__theme-toggler");

HTML_ELEMENT.dataset.theme =
  JSON.parse(localStorage.getItem("current-theme")) || "light";

function handleClick(ev) {
  ev.stopPropagation();

  const currentTheme = JSON.parse(localStorage.getItem("current-theme")) || HTML_ELEMENT.dataset.theme;

  HTML_ELEMENT.dataset.theme = currentTheme === "light" ? "dark" : "light";

  localStorage.setItem(
    "current-theme",
    JSON.stringify(HTML_ELEMENT.dataset.theme)
  );
}

themeToggler.addEventListener("click", handleClick);
//////////////////////////navbar//////////////////////////////////////
const nav = document.querySelector(".header__nav")
let isNavOpen = false
const collapseNav = () => {
  isNavOpen = !isNavOpen
  nav.style.right = isNavOpen ?  "0" : "-350px"
}
/////////////////////search input//////////////////////////////////////
const form = document.querySelector(".search-form")
const brand = document.querySelector(".header__brand")
const moveInput = () => {
  form.classList.add("searching")
  brand.classList.add("brand-searching")
}