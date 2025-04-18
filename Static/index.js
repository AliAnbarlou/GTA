const HTML_ELEMENT = document.documentElement,
  themeToggler = document.querySelector(".header__theme-toggler");

HTML_ELEMENT.dataset.theme =
  JSON.parse(localStorage.getItem("current-theme")) || "dark";

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
  nav.style.right = isNavOpen ? "0" : "-350px"
}
/////////////////////search input//////////////////////////////////////
const form = document.querySelector(".search-form")
const brand = document.querySelector(".header__brand")
const moveInput = () => {
  form.classList.add("searching")
  brand.classList.add("brand-searching")
}
//////////////////////suggestions/////////////////////////////////////
const suggestionsDiv = document.querySelector(".suggestions")
const suggestionsList = document.querySelector(".suggestions-list")
let suggestions = []
let timeout;
const debounce = (search) => {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    if (search.trim().length >= 2) {
      getSuggestions(search)
    }
    else if (search.trim().length == 0) {
      suggestionsDiv.style.height = 0
    }
  }, 300);
}
const getSuggestions = async (search) => {
  await axios.get(`${window.location.origin}/word/api/${search}`).then((res) => {
    suggestions = res.data.hits
  }).catch((err) => {
    console.error(err);
  })
  suggestionsList.innerHTML = ""
  if (suggestions.length >= 1){
    suggestions.forEach((item, index) => {
      if (index <= 4) {
        suggestionsList.innerHTML += `<li class="suggestions-list-item">${item.title}</li>`
      }
    })
  }
  else {
    suggestionsList.innerHTML = `<li class="suggestions-list-item">موردی یافت نشد</li>`
  }
  suggestionsDiv.style.height = `${suggestionsList.getBoundingClientRect().height}px`
}
