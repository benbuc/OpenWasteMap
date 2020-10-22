function getLocation() {
    if (navigator.geolocation) {
        document.getElementById("gpsAccuracy").innerHTML = "Getting Position...";
        navigator.geolocation.getCurrentPosition(updatePosition, errorGettingPosition);
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}

function updatePosition(position) {
    console.log(position);
    var longitudeInput = document.getElementById("id_longitude");
    var latitudeInput = document.getElementById("id_latitude");

    longitudeInput.value = position.coords.longitude.toFixed(6);
    latitudeInput.value = position.coords.latitude.toFixed(6);
    document.getElementById("gpsAccuracy").innerHTML = position.coords.accuracy;
}

function errorGettingPosition(error) {
    console.log(error);
    document.getElementById("gpsAccuracy").innerHTML = "Error " + error.code + ": " + error.message;
}