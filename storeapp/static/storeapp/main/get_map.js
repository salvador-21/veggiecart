

 // Initialize the map
// var map = L.map('map').setView([0, 0], 2); 
var map = L.map("map", {
    crs: L.CRS.EPSG3857, // Default
}).setView([0, 0], 2);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var markersLayer = L.layerGroup().addTo(map);
var userMarker = L.marker([0, 0], { draggable: true }).addTo(markersLayer);
// Locate the user and add a marker
map.locate({ setView: true, maxZoom: 16, enableHighAccuracy: true });

map.on('locationfound', function (e) {
    // userMarker = L.marker(e.latlng).addTo(map).bindPopup("📍 You are here!").openPopup();
    map.setView([e.latlng.lat, e.latlng.lng], 13);
    getAddress(e.latlng.lat, e.latlng.lng)
});

userMarker.on('dragend', function (event) {
    var position = userMarker.getLatLng(); // Get new marker position
    getAddress(position.lat, position.lng);
    
    // console.log("New Location:", position.lat, position.lng);
    // alert(`📍 Marker moved to:\nLatitude: ${position.lat}\nLongitude: ${position.lng}`);
});





function getAddress(lat, lng) {
    var url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var address = data.display_name;
            // console.log(data)
            // console.log(data.lat)
            // console.log(data.lon)
            userMarker.setLatLng([data.lat, data.lon], { draggable: true }).bindPopup(address).openPopup();
            $('#ad_name').val(data.display_name)
            $('#ad_lat').val(data.lat)
            $('#ad_lng').val(data.lon)
            $('#state').val(data.address.state)
            $('#region').val(data.address.region)
        })
        .catch(error => console.error("Error fetching address:", error));
}

function searchLocation() {
    // markersLayer.clearLayers();
    var query = document.getElementById('search-box').value;
    var url = `https://nominatim.openstreetmap.org/search?format=json&q=${query}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                var lat = data[0].lat;
                var lng = data[0].lon;
                map.setView([lat, lng], 13);
                // console.log("Found Location:", lat, lng);
                getAddress(lat, lng)
              
            } else {
                alert("⚠️ Location not found!");
            }
        })
        .catch(error => console.error("Error:", error));
}

// Handle errors
map.on('locationerror', function () {
    console.log("⚠️ Location access denied or unavailable!");
});

document.getElementById("MapModal").addEventListener("shown.bs.modal", function () {
    setTimeout(() => {
        map.invalidateSize(); // Recalculate map size after modal is shown
    }, 300); // Slight delay to allow modal animations to complete
});

