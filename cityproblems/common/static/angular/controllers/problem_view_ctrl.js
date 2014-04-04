var problemViewCtrl = function ($scope)
{
    "use strict";
    function setMarker(latLng)
    {
        var marker = new google.maps.Marker({
            position: latLng,
            map: $scope.map,
        });
    }

    $scope.map_init=function()
    {
        if(!$scope.zoom)
            $scope.zoom =11;
        var latLng = new google.maps.LatLng(parseFloat($scope.latitude.replace(",", ".")), parseFloat($scope.longitude.replace(",", ".")));
        var mapOptions = {
            zoom: parseInt($scope.zoom),
            center: latLng,
            scrollwheel: false,
        }
        $scope.map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        if($scope.latitude != 0 && $scope.longitude != 0)
        {
           setMarker(latLng);
        }        
    }    
};
problemViewCtrl.$inject = ["$scope"];