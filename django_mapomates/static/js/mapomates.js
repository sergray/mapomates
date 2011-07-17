var profiles = [];

var Map;

var ProfileIcon = L.Icon.extend({
    iconUrl: STATIC_URL+'img/mapicons/number_0.png',
    shadowUrl: STATIC_URL+'img/mapicons-odesk/shadow.png',
    iconSize: new L.Point(28, 45),
    shadowSize: new L.Point(50, 45),
    iconAnchor: new L.Point(14, 45),
});


function profile_url(cipher_text) {
    return 'https://www.odesk.com/users/' + cipher_text;
}


function createMarker2 (profile, number) {
    var iconUrl = STATIC_URL;
    if(number==0) 
        iconUrl += 'img/mapicons-odesk/special.png';
    else
        iconUrl += 'img/mapicons-odesk/number_'+number+'.png';
    var markerIcon = new ProfileIcon(iconUrl);
    var markerLocation = new L.LatLng(Number(profile.lat), Number(profile.lon));
    if (profile.username == USERNAME) {
        var marker = new L.Marker(markerLocation, {icon: markerIcon, draggable: true});
    }
    else {
        var marker = new L.Marker(markerLocation, {icon: markerIcon});
    }
    var popupHTML = ""+ 
        "<table style='width:200px'>" +
            "<tr>"+
                "<td><img src='"+profile.portrait+"'/></td><td><p><strong><a href='"+profile_url(profile.cipher_text)+"'>"+profile.full_name+"</a></strong></p><p>"+profile.location+"</p></td>"+
            "<tr>"+
        "</table>" +
    "";
    marker.bindPopup(popupHTML, {maxWidth: 400});
    Map.addLayer(marker);
    var profileHTML = ""+ 
        "<tr>"+
            "<td><img src='"+iconUrl+"'/></td>"+
            "<td><img src='"+profile.portrait+"'/></td>"+
            "<td>" +
            "<p><strong><a href='"+profile_url(profile.cipher_text)+"' target='_blank'>"+profile.full_name+"</a></strong>"+
            "<p>"+profile.location+"</p></td>"+
        "<tr>"+
    "";
    $('#profiles table').append($(profileHTML));
    return marker;
}

function proxy_url(url) {
    return PROXY_URL+'?url='+encodeURIComponent(url); 
}


function update_coords(profile_index) {
    var profile = profiles[profile_index];
    url = "http://nominatim.openstreetmap.org/search?format=json&q="+profile.location.replace(' ','+');
    $.get(proxy_url(url), function (data) {
        var result = $.parseJSON(data);
        profile.coords[0] = Number(result[0].lat);
        profile.coords[1] = Number(result[0].lon);
        createMarker2(profile, profile_index);
    });
}

function on_odesk_profile(data, index) {
    console.log(data);
    var profile = data;
    console.log('SUCCESS ')
    console.log(profile);
    if (profile.portrait == '') 
        profile.portrait = STATIC_URL+'img/noimage.png';
    createMarker2(profile, index);
}

$(document).ready(function () {

    var map = new L.Map('map');
    console.log('success');
    //var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png';
    var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/'+CLOUDMADE_KEY+'/'+CLOUDMADE_THEME+'/256/{z}/{x}/{y}.png';
    var cloudmadeAttrib = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade';
    var cloudmade = new L.TileLayer(cloudmadeUrl, {maxZoom: 18, attribution: cloudmadeAttrib});
   
    var london = new L.LatLng(51.505, -0.09); 
    map.setView(london, 2).addLayer(cloudmade);
    Map = map;

    $.each(PROFILES, function (index, ciphertext) {
        //var url = 'http://www.odesk.com/api/profiles/v1/providers/'+ciphertext+'/brief.json';
        var url = '/profile/'+ciphertext+'/';
        $.get(url, function(data) {
            on_odesk_profile(data, index);
        });
    });
    
    
})
