// Script needs to be run on each of the `http://ashrae-meteo.info/v2.0` stations pages. 
// At the time of writing, there are Asia, North America, Latin America, Australia and Oceania, Europe, Africa, Antarctica pages.

// Stations Pages
// http://ashrae-meteo.info/v2.0/places.php?continent=Asia
// http://ashrae-meteo.info/v2.0/places.php?continent=North%20America
// http://ashrae-meteo.info/v2.0/places.php?continent=Latin%20America
// http://ashrae-meteo.info/v2.0/places.php?continent=Australia%20and%20Oceania
// http://ashrae-meteo.info/v2.0/places.php?continent=Europe
// http://ashrae-meteo.info/v2.0/places.php?continent=Africa
// http://ashrae-meteo.info/v2.0/places.php?continent=Antarctica

function getAllStations() {
    var links = document.querySelectorAll('#accordion a[target=_blank]');
    var accordian = document.getElementById('accordion');

    var stations = [];
    
    for (var i = 0; i < links.length; i++) {
        var link = links[i];

        var station = {};
        
        station.name = link.innerText;
        
        var urlParams = new URL(link.href).searchParams;
        
        station.lat = urlParams.get('lat');
        station.lng = urlParams.get('lng');
        station.wmo = urlParams.get('wmo');

        station.parents = [];

        var el = link;

        while (el != accordian) {
            el = el.parentElement;
            if (el == accordian) break;
            el = el.previousSibling;
            station.parents.push(el.innerText);
        }

        stations.push(station);
    }
    
    return stations;
}

getAllStations();
