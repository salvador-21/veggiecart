// Initialize the map

var map = L.map('map').setView([0, 0], 13); 

// Load OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

var markersLayer = L.layerGroup().addTo(map);
var userMarker = L.marker([0, 0], { draggable: true }).addTo(markersLayer);

// Watch the user's real-time location
function updateLocation(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;

    userMarker.setLatLng([lat, lng], { draggable: true });
    
    map.setView([lat, lng], 16);

    var url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            
            var address = data.display_name;
            
            
            userMarker.bindPopup(address).openPopup();
            $('#ad_name').val(data.display_name)
            $('#ad_lat').val(data.lat)
            $('#ad_lng').val(data.lon)
        })
        .catch(error => console.error("Error fetching address:", error));

}

// Add a marker for the user


// Listen for marker drag event
userMarker.on('dragend', function (event) {
    var position = userMarker.getLatLng(); // Get new marker position
    getAddress(position.lat, position.lng);
    
    // console.log("New Location:", position.lat, position.lng);
    // alert(`📍 Marker moved to:\nLatitude: ${position.lat}\nLongitude: ${position.lng}`);
});

// Handle location errors
function handleError(error) {
    console.error("Error getting location: ", error.message);
}

// Start tracking the user's location
if ("geolocation" in navigator) {
    navigator.geolocation.watchPosition(updateLocation, handleError, {
        enableHighAccuracy: true, // High accuracy mode
        // maximumAge: 0, // No cached locations
        // timeout: 10000 // 10 seconds timeout
    });
} else {
    alert("Geolocation is not supported by your browser.");
}


function getAddress(lat, lng) {
    var url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var address = data.display_name;
            console.log("Address:", address);
       
            $('#ad_name').val(data.display_name)
            $('#ad_lat').val(data.lat)
            $('#ad_lng').val(data.lon)
            userMarker.bindPopup(address).openPopup();
        })
        .catch(error => console.error("Error fetching address:", error));
}

function searchLocation() {
    markersLayer.clearLayers();
    var query = document.getElementById('search-box').value;
    var url = `https://nominatim.openstreetmap.org/search?format=json&q=${query}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                var lat = data[0].lat;
                var lng = data[0].lon;
                $('#ad_name').val(data[0].display_name)
                $('#ad_lat').val(data[0].lat)
                $('#ad_lng').val(data[0].lon)
                console.log("Found Location:", lat, lng);
                
                // Center map on new location
                map.setView([lat, lng], 13);
                var userMarker = L.marker([lat, lng], { draggable: true }).addTo(markersLayer);
                userMarker.on('dragend', function (event) {
                    var position = userMarker.getLatLng(); // Get new marker position
                    var url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${position.lat}&lon=${position.lng}`;
    
                    fetch(url)
                        .then(response => response.json())
                        .then(data => {
                            
                            var address = data.display_name;
                            console.log("Address:", address);
                            
                            userMarker.bindPopup(address).openPopup();
                            $('#ad_name').val(data.display_name)
                            $('#ad_lat').val(data.lat)
                            $('#ad_lng').val(data.lon)
                            
                        })
                        .catch(error => console.error("Error fetching address:", error));
                });
              
            } else {
                alert("⚠️ Location not found!");
            }
        })
        .catch(error => console.error("Error:", error));
}
