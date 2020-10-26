function getLocation() {

    var options = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
    };

    if (navigator.geolocation) {
        document.getElementById("gpsAccuracy").innerHTML = "Getting Position...Please Wait";
        navigator.geolocation.getCurrentPosition(updatePosition, errorGettingPosition, options);
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}

function updatePosition(position) {
    var latitudeInput = document.getElementById("id_latitude");
    var longitudeInput = document.getElementById("id_longitude");

    latitudeInput.value = position.coords.latitude.toFixed(6);
    longitudeInput.value = position.coords.longitude.toFixed(6);
    document.getElementById("gpsAccuracy").innerHTML = position.coords.accuracy + "m";
}

function errorGettingPosition(error) {
    document.getElementById("gpsAccuracy").innerHTML = "Error " + error.code + ": " + error.message;
}