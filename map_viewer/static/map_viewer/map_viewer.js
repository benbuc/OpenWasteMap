function registerMap() {
    var owmMap = L.map('owm-map').setView([52.5183, 13.4006], 11);
    var tileUrl = document.getElementById('owm-map').getAttribute('data-tile-url');

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
    }).addTo(owmMap);
    L.tileLayer(tileUrl + '{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(owmMap);

    L.control.scale().addTo(owmMap)
}

document.addEventListener("DOMContentLoaded", registerMap);