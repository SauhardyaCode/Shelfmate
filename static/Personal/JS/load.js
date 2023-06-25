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

document.getElementsByTagName('form')[0].addEventListener('submit', () => {
    document.getElementsByTagName('main')[0].style.display = 'none';
})