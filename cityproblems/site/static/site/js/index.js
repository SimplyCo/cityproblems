var mainPageViewCtrl = function ($scope)
{
    "use strict";
    $scope.showMenu = false;
    function setMarker(latLng)
    {
        var marker = new google.maps.Marker({
            position: latLng,
            map: $scope.map,
        });
    }

    $scope.map_init=function()
    {
        var zoom = parseInt($scope.zoom);
        if(zoom!=zoom)
            $scope.zoom=11;
        var latitude = parseFloat($scope.latitude.replace(",", "."));
        var longitude = parseFloat($scope.longitude.replace(",", "."));
        if(latitude!=latitude || longitude!=longitude)
        {
            alert("Wrong map config. Please fix it in site parameters");
            return;
        }
        var latLng = new google.maps.LatLng(latitude, longitude);
        var mapOptions = {
            zoom: zoom,
            center: latLng,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false
        }
        $scope.map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    }
};
mainPageViewCtrl.$inject = ["$scope"];