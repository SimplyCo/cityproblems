var mainPageViewCtrl = function ($scope, $http, $route)
{
    "use strict";
    $scope.showMenu = false;
    $scope.alerts=[];
    
    $scope.$on('$routeChangeSuccess', function(next, current)
    {
        if((current.params.reportBy != $scope.reportBy || current.params.category != $scope.category) && (typeof current.params.reportBy != "undefined" && typeof current.params.category != "undefined"))
        {
            $scope.reportBy = current.params.reportBy;
            $scope.category = current.params.category;
            loadMarkers();
        }
    });
    
    $scope.init=function(categories)
    {
        $scope.categories = angular.fromJson(categories);
        $scope.tmpCategory = "all";
    }
    
    $scope.$watch("category", function(category, oldValue)
    {
        if(category != oldValue)
            for(var i=0;i<$scope.categories.length;++i)
                if($scope.categories[i]["url_name"] == category)
                {
                    $scope.categoryTitle = $scope.categories[i].title;
                    break;
                }                
    }
    )
    
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
    }
    
    function loadMarkers()
    {
        $http.post($scope.loadDataURL, {reportBy: $scope.reportBy, category: $scope.category})
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
    
    $scope.closeAlert = function(index)
    {
        $scope.alerts.splice(index, 1);
    };
};
mainPageViewCtrl.$inject = ["$scope", "$http", "$route"];
