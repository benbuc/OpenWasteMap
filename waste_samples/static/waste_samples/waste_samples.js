function getLocation() {
    if (navigator.geolocation) {
        document.getElementById("gpsAccuracy").innerHTML = "Getting Position...";
        navigator.geolocation.getCurrentPosition(updatePosition);
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}

function updatePosition(position) {
    var longitudeInput = document.getElementById("id_longitude");
    var latitudeInput = document.getElementById("id_latitude");

    longitudeInput.value = position.coords.longitude.toFixed(6);
    latitudeInput.value = position.coords.latitude.toFixed(6);
    document.getElementById("gpsAccuracy").innerHTML = position.coords.accuracy;
}