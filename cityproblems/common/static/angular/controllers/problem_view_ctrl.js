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