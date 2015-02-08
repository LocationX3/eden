/**
* Ask user for permission to share location
*/
navigator.geolocation.getCurrentPosition(function (position) {
	var maps = S3.gis.maps;
	var localZoom = 15;
    var map_id;
    for (map_id in maps) {
    	var map = S3.gis.maps[map_id];
        var lonlat = new OpenLayers.LonLat(position.coords.longitude, position.coords.latitude);
        map.setCenter(lonlat, localZoom);
    }
});
