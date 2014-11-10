var pageContent;

var options = {
  maximumAge: 0,
  enableHighAccuracy: true,
  timeout: Infinity,
};

function getLocation() {
    if (navigator.geolocation) {
        positionRequest = navigator.geolocation.getCurrentPosition(success, failure, options);
    } else {
        pageContent = "<strong>Yikes!</strong> Your browser does not support this feature.";
        document.write(pageContent);
    }
};

function success(position) {
    var coordinates = position.coords;
    //coordinates.latitude, coordinates.longitude
    var imgURL = "//maps.googleapis.com/maps/api/staticmap?center=" + coordinates.latitude + "," + coordinates.longitude + "&zoom=14&size=400x400";
    var imgHTML = '<img src="' + imgURL + '">';
    pageContent = "Your location is: <br><br>";
    pageContent += imgHTML; 
    document.write(pageContent);
};

function failure(position_error) {
    pageContent = "<strong>Uh oh!</strong> We weren't able to determine your location. Try hitting 'Allow' on the browser permissions prompt or changing your settings.";
    document.write(pageContent);
};

getLocation();
