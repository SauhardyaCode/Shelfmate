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

function show_loader() {
    let main = document.getElementsByTagName('main')[0]
    setTimeout(() => {
        try {
            main.innerHTML += `<div class="show" id="loading"><div id="loading-content">
                    <div class="loader"></div>
                    </div></div>`
        }
        catch { }
    }, 500);
}

const all_forms = document.getElementsByTagName('form')
for (i in all_forms) {
    try {
        all_forms[i].addEventListener('submit', show_loader)
    }
    catch { }
}

window.addEventListener('unload', () => {
    if (window.opener && window.opener != window) {
        document.getElementById('loading').remove()
    }
})

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}