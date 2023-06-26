const load = `<div id="loading-content">
<div class="loader"></div>
</div>`

const position = document.getElementById('loading');
position.innerHTML = load;

window.addEventListener('load', () => {
    var loadingScreen = document.getElementById('loading');
    loadingScreen.classList.remove('show');
    setInterval(() => {
        loadingScreen.style.display = "none";
    }, 500);
});

const all_forms = document.getElementsByTagName('form')
all_forms[all_forms.length - 1].addEventListener('submit', () => {
    let main = document.getElementsByTagName('main')[0]
    main.style.backgroundColor = "white";
    setTimeout(() => {
        main.innerHTML += `<div class="show" id="loading"><div id="loading-content">
                <div class="loader"></div>
                </div></div>`
    }, 1000);
})