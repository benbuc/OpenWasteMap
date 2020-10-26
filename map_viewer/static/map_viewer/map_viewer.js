function registerMap() {
    var owm_map = L.map('owm-map').setView([52.5183, 13.4006], 11);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
    }).addTo(owm_map);

    L.control.scale().addTo(owm_map)
}

document.addEventListener("DOMContentLoaded", registerMap);