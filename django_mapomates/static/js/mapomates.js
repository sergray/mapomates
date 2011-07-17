var username_cache = [];

$(document).ready(function () {
    var map = new L.Map('map');
    console.log('success');
    //var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png';
    var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/'+CLOUDMADE_KEY+'/'+CLOUDMADE_THEME+'/256/{z}/{x}/{y}.png';
    var cloudmadeAttrib = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade';
    var cloudmade = new L.TileLayer(cloudmadeUrl, {maxZoom: 18, attribution: cloudmadeAttrib});
   
    var london = new L.LatLng(51.505, -0.09); 
    map.setView(london, 2).addLayer(cloudmade);


    /*var ProfileIcon = L.Icon.extend({
        iconUrl: STATIC_URL+'img/mapicons/number_0.png',
        shadowUrl: STATIC_URL+'img/mapicons/shadow.png',
        iconSize: new L.Point(32, 37),
        shadowSize: new L.Point(51, 37),
        //iconAnchor: new L.Point(22, 94),
        //popupAnchor: new L.Point(-3, -76)
    });*/

    var ProfileIcon = L.Icon.extend({
        iconUrl: STATIC_URL+'img/mapicons/number_0.png',
        shadowUrl: STATIC_URL+'img/mapicons-odesk/shadow.png',
        iconSize: new L.Point(28, 45),
        shadowSize: new L.Point(50, 45),
        iconAnchor: new L.Point(14, 45),
        //popupAnchor: new L.Point(-3, -76)
    });

    function createMarker (profile, number) {
        if (profile.username == USERNAME) {
            var iconUrl = STATIC_URL+'img/mapicons-odesk/special.png';
        }
        else {
            var iconUrl = STATIC_URL+'img/mapicons-odesk/number_'+number+'.png';
        }
        var markerIcon = new ProfileIcon(iconUrl);
        var markerLocation = new L.LatLng(profile.coords[0], profile.coords[1]);
        if (profile.username == USERNAME) {
            var marker = new L.Marker(markerLocation, {icon: markerIcon, draggable: true});
        }
        else {
            var marker = new L.Marker(markerLocation, {icon: markerIcon});
        }
        //var marker = new L.Marker(markerLocation);
        //marker.bindPopup("<p><strong>"+profile.name+"</strong></p><p>"+profile.location+"</p>");
        var popupHTML = ""+ 
            "<table style='width:260px'>" +
                "<tr>"+
                    "<td><img src='"+profile.pic+"'/></td><td><p><strong>"+profile.name+"</strong></p><p>"+profile.location+"</p></td>"+
                "<tr>"+
            "</table>" +
        "";
        marker.bindPopup(popupHTML, {maxWidth: 400});
        map.addLayer(marker);
        return marker;
    }
    
    $.get(PROFILES_URL, function (data) {
        var profiles = $.parseJSON(data);
        //var profiles = data;
        console.log(profiles);
        $.each(profiles, function (index, profile) {
            
            if (username_cache.indexOf(profile.username) > -1) {
                //Don't do anything if this profile was already processed
                return 
            }
            username_cache.push(profile.username);
            createMarker(profile, index+1);

            console.log(profile);
            //var markerIcon = new ProfileIcon(profile.pic);
            if (profile.username == USERNAME) {
                var iconUrl = STATIC_URL+'img/mapicons-odesk/special.png';
            }
            else {
                var iconUrl = STATIC_URL+'img/mapicons-odesk/number_'+(index+1)+'.png';
            }
            var profileHTML = ""+ 
                "<tr>"+
                    "<td><img src='"+iconUrl+"'/></td>"+
                    "<td><img src='"+profile.pic+"'/></td>"+
                    "<td><p><strong>"+profile.name+"</strong></p><p>"+profile.location+"</p></td>"+
                "<tr>"+
            "";
            $('#profiles table').append($(profileHTML));
        })
    });
    
})
