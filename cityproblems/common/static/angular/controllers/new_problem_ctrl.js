var NewProblemCtrl = function ($scope, $upload, $http, $timeout)
{
    "use strict";
    function setMarker(latLng)
    {
        var marker = new google.maps.Marker({
            position: latLng,
            map: $scope.map,
            draggable: true
        });
        google.maps.event.addListener(marker, 'dragend', function()
        {
            var latLng = marker.getPosition();
            document.getElementsByName("latitude")[0].value=latLng.lat();
            document.getElementsByName("longitude")[0].value=latLng.lng();
        });
    }

    $scope.map_init=function()
    {
        $scope.latitude=document.getElementsByName("latitude")[0].value;
        $scope.longitude=document.getElementsByName("longitude")[0].value;
        var latitude = $scope.latitude==0 ? $scope.default_latitude : $scope.latitude;
        var longitude = $scope.longitude==0 ? $scope.default_longitude : $scope.longitude;
        var latLng = new google.maps.LatLng(parseFloat(latitude.replace(",", ".")), parseFloat(longitude.replace(",", ".")));
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
        else
        {
            var clickListener = google.maps.event.addListener($scope.map, 'click', function(event) 
            {
                var latLng = event.latLng;
                document.getElementsByName("latitude")[0].value=latLng.lat();
                document.getElementsByName("longitude")[0].value=latLng.lng();
                setMarker(latLng);
                google.maps.event.removeListener(clickListener);
            });
        }
    }

    
    
    
    $scope.files=[];
    $scope.alerts=[];
    $scope.onFileSelect = function($files)
    {  
        for(var i=0; i<$files.length; ++i)
        {
            $scope.files.push({"file": $files[i]});
            $scope.start($scope.files.length-1);
        }
    }
    
    $scope.start=function(index)
    {
        $scope.isUploadingNow=true;
        $scope.$apply();
        var file = $scope.files[index];
        file.progress=0;
        file.upload = $upload.upload({
            url: $scope.uploadURL,
            method: "POST",
            data: {id: $scope.id},
            file: file.file,
      }).progress(function(evt) {
        file.progress = parseInt(100.0 * evt.loaded / evt.total);
      }).success(function(data, status, headers, config) {
          if ("Error" in data)
          {
                $scope.alerts.push({type: 'danger', msg: data.Error});
                $scope.files.splice($scope.files.indexOf(file), 1);
          }
          else
          {
                if (window.FileReader && file.file.type.indexOf('image') > -1) 
                {
                    var fileReader = new FileReader();
                    fileReader.readAsDataURL(file.file);
                    fileReader.onload = function(e) 
                    {
                        $timeout(function() {
                                file.thumbnail = e.target.result;
                                file.file = null;
                        });
                    }
                }else
                {
                    file.thumbnail = data.thumbnail;
                    file.file = null;
                }
                file.id = data.id;
                file.url = data.url;
                file.order_number = data.order_number;
                file.name = file.file.name;
                file.upload = null;
          }
            $scope.isUploadingNow=false;
      }).error(function(data){
          //document.write(data);
          $scope.files.splice($scope.files.indexOf(file), 1);
          if(!$scope.isAborted)
            $scope.alerts.push({type: 'danger', msg: "Error. Something happend while upload file."});
          else
             $scope.isAborted=false; 
             $scope.isUploadingNow=false;
      });
    }
    
    $scope.abort=function(file)
    {
        file.upload.abort(); 
        $scope.isAborted=true;
    }
    
    $scope.remove=function(file)
    {
        $http.post($scope.removeURL, {"id": file.id})
                .success(function(data)
                {
                    if ("Error" in data)
                        $scope.alerts.push({type: 'danger', msg: data["Error"]});
                    else
                    {
                        $scope.files.splice($scope.files.indexOf(file), 1);
                    }
                })
                .error(function(data)
                {
                    //document.write(data);
                    $scope.alerts.push({type: 'danger', msg: "Error while delete file"});
                });
    }
    
    $scope.init=function(files)
    {
        $scope.files=angular.fromJson(atob(files));
    }
    
    $scope.closeAlert = function(index)
    {
        $scope.alerts.splice(index, 1);
    };
    
    $scope.moveImage=function(file, action)
    {
        $http.post($scope.moveURL, {"id": file.id, "action": action})
                .success(function(data)
                {
                    if ("Error" in data)
                        $scope.alerts.push({type: 'danger', msg: data["Error"]});
                    else
                    {
                        $scope.files.sort(function(a,b){return a["order_number"]-b["order_number"]});
                        var index = $scope.files.indexOf(file);
                        $scope.files[index+action]["order_number"] += $scope.files[index]["order_number"];
                        $scope.files[index]["order_number"] = $scope.files[index+action]["order_number"] - $scope.files[index]["order_number"];
                        $scope.files[index+action]["order_number"] -= $scope.files[index]["order_number"];
                    }
                })
                .error(function(data)
                {
                    //document.write(data);
                    $scope.alerts.push({type: 'danger', msg: "Error while move image"});
                });
    }
};
NewProblemCtrl.$inject = ["$scope", "$upload", "$http", "$timeout"];