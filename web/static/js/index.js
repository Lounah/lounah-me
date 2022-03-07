const THEME_KEY = 'theme';
const LIGHT_THEME = 'theme-light';
const DARK_THEME = 'theme-dark';

(function () {
    window.onpageshow = function(event) {
        if (event.persisted) {
            window.location.reload();
        }
    };

    if (localStorage.getItem(THEME_KEY) === DARK_THEME) {
        setDarkTheme();
    } else {
        setLightTheme();
    }
})();

function updateLanguage(code) {
    document.cookie = "lang" + "=" + code + ';path=/';
    window.location.reload();
}

function setTheme(theme) {
    localStorage.setItem(THEME_KEY, theme);
    document.documentElement.className = theme;
}

function setLightTheme() {
    setTheme(LIGHT_THEME);
    document.getElementById("code").setAttribute("href", "/css/code/github-light.css");
}

function setDarkTheme() {
    setTheme(DARK_THEME);
    document.getElementById("code").setAttribute("href", "/css/code/github-dark.css");
}
