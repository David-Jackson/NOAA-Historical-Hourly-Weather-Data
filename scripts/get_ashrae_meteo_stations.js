// Run on page like http://ashrae-meteo.info/v2.0/places.php?continent=North%20America

// Stations Pages
// http://ashrae-meteo.info/v2.0/places.php?continent=Asia
// http://ashrae-meteo.info/v2.0/places.php?continent=North%20America
// http://ashrae-meteo.info/v2.0/places.php?continent=Latin%20America
// http://ashrae-meteo.info/v2.0/places.php?continent=Australia%20and%20Oceania
// http://ashrae-meteo.info/v2.0/places.php?continent=Europe
// http://ashrae-meteo.info/v2.0/places.php?continent=Africa
// http://ashrae-meteo.info/v2.0/places.php?continent=Antarctica


async function loadStationPages() {

    var allStations = []
    
    var stationPages = [
        "http://ashrae-meteo.info/v2.0/places.php?continent=Asia",
        "http://ashrae-meteo.info/v2.0/places.php?continent=North%20America",
        "http://ashrae-meteo.info/v2.0/places.php?continent=Latin%20America",
        "http://ashrae-meteo.info/v2.0/places.php?continent=Australia%20and%20Oceania",
        "http://ashrae-meteo.info/v2.0/places.php?continent=Europe",
        "http://ashrae-meteo.info/v2.0/places.php?continent=Africa",
        "http://ashrae-meteo.info/v2.0/places.php?continent=Antarctica",
    ]

    for (var i = 0; i < stationPages.length; i++) {
    
        var url = stationPages[i];

        console.log("Loading", url);
        
        var response = await fetch(url);
        var text = await response.text();
    
        var parser = new DOMParser();
        var htmlDoc = parser.parseFromString(text, 'text/html');
    
        var newStations = getAllStations(htmlDoc);

        console.log("Found", newStations.length, "new stations");
    
        allStations = allStations.concat(newStations);

    }

    return allStations;

}

function getAllStations(htmlDoc) {
    var links = htmlDoc.body.querySelectorAll('#accordion a[target=_blank]');
    var accordian = htmlDoc.getElementById('accordion');

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

await loadStationPages();
