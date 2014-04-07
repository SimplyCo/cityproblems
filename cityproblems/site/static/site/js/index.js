var mainPageViewCtrl = function ($scope, $http)
{
    "use strict";
    $scope.showMenu = false;
    $scope.alerts=[];
    
    function clearMap()
    {
        if(!$scope.markers)
        {
            $scope.markers=[];
            return;
        }
        for(var i=0;i<$scope.markers.length;++i)
            $scope.markers[i].setMap(null);
        $scope.markers=[];
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
        $scope.reportBy = "all";
    }
    
    function loadMarkers()
    {
        var sendDict={reportBy: $scope.reportBy};
        $http.post($scope.loadDataURL, sendDict)
                .success(function(data)
                {
                    if ("error" in data)
                        $scope.alerts.push({type: 'danger', msg: data["error"]});
                    else
                    {
                        clearMap();
                        var objList = data["problems"];
                        var infowindow = new google.maps.InfoWindow();
                        $scope.infowindow=infowindow;
                        for(var i=0;i<objList.length;++i)
                        {
                            var myLatlng = new google.maps.LatLng(parseFloat(objList[i].latitude), parseFloat(objList[i].longitude));
                            var marker = new google.maps.Marker({
                                position: myLatlng,
                                map: $scope.map,
                                html: '<a href="'+$scope.problemViewURL+objList[i].id+'/" target="_blank">'+objList[i].title+'</a>'
                            });                        
                        google.maps.event.addListener(marker, 'click', function () 
                            {
                                infowindow.setContent(this.html);
                                infowindow.open($scope.map, this);
                        });                        
                        $scope.markers.push(marker);       
                        }
                    }
                })
                .error(function(data)
                {
                    //document.write(data);
                    $scope.alerts.push({type: 'danger', msg: "Error while load data"});
                });
    }
    
    $scope.$watch("reportBy", function()
    {
        loadMarkers();
    }
    )
    
    $scope.closeAlert = function(index)
    {
        $scope.alerts.splice(index, 1);
    };
};
mainPageViewCtrl.$inject = ["$scope", "$http"];
