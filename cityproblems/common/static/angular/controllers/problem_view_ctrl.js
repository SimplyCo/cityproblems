var problemViewMapCtrl = function ($scope)
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
            scrollwheel: false,
        }
        $scope.map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        if($scope.latitude != 0 && $scope.longitude != 0)
        {
           setMarker(latLng);
        }        
    }    
};
problemViewMapCtrl.$inject = ["$scope"];

var problemViewCtrl = function ($scope, $http)
{
    "use strict";
    $scope.init=function(statuses, status)
    {
        $scope.statuses=angular.fromJson(atob(statuses));
        $scope.status=status;
    }
    
    $scope.$watch('status', function(status, oldValue)
    {
        if(status == oldValue)
            return;
        $http.post($scope.statusChangeURL, {"status": $scope.status})
                .success(function(data)
                {
                    if ("Error" in data)
                        $scope.alerts.push({type: 'danger', msg: data["Error"]});
                    else
                        $scope.alerts.push({type: 'success', msg: data["success"]});
                })
                .error(function()
                {
                    $scope.alerts.push({type: 'danger', msg: "Error while change status"});
                });
    });
}
problemViewCtrl.$inject = ["$scope", "$http"];
