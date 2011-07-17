var username_cache = [];

var profiles = [];

var Map;

var ProfileIcon = L.Icon.extend({
    iconUrl: STATIC_URL+'img/mapicons/number_0.png',
    shadowUrl: STATIC_URL+'img/mapicons-odesk/shadow.png',
    iconSize: new L.Point(28, 45),
    shadowSize: new L.Point(50, 45),
    iconAnchor: new L.Point(14, 45),
    //popupAnchor: new L.Point(-3, -76)
});


function createMarker2 (profile, number) {
    var iconUrl = STATIC_URL+'img/mapicons-odesk/number_'+number+'.png';
    var markerIcon = new ProfileIcon(iconUrl);
    var markerLocation = new L.LatLng(profile.coords[0], profile.coords[1]);
    if (profile.username == USERNAME) {
        var marker = new L.Marker(markerLocation, {icon: markerIcon, draggable: true});
    }
    else {
        var marker = new L.Marker(markerLocation, {icon: markerIcon});
    }
    var popupHTML = ""+ 
        "<table style='width:260px'>" +
            "<tr>"+
                "<td><img src='"+profile.pic+"'/></td><td><p><strong>"+profile.name+"</strong></p><p>"+profile.location+"</p></td>"+
            "<tr>"+
        "</table>" +
    "";
    marker.bindPopup(popupHTML, {maxWidth: 400});
    Map.addLayer(marker);
    var profileHTML = ""+ 
        "<tr>"+
            "<td><img src='"+iconUrl+"'/></td>"+
            "<td><img src='"+profile.pic+"'/></td>"+
            "<td><p><strong>"+profile.name+"</strong></p><p>"+profile.location+"</p></td>"+
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

function on_odesk_profile(data) {
    var result = $.parseJSON(data);
    var profile = result['profile'];
    profile.name = profile['dev_full_name'];
    profile.location = profile['dev_city']+', '+profile['dev_country'];
    profile.pic = profile['dev_portrait_50'];
    profile.pic_small = profile['dev_portrait_32'];
    profile.coords = [0, 0];
    index = profiles.push(profile)-1;
    update_coords(index);
}

function on_odesk_search(data) {
    var result = $.parseJSON(data);
    $.each(result['providers']['provider'], function (index, provider) {
        var url = 'http://www.odesk.com/api/profiles/v1/providers/'+provider['ciphertext']+'/brief.json';
        $.get(proxy_url(url), on_odesk_profile);
    })
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
        var url = 'http://www.odesk.com/api/profiles/v1/providers/'+ciphertext+'/brief.json';
        console.log(url);
        $.get(proxy_url(url), on_odesk_profile);
    });
    
    /*
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
    */
    
})