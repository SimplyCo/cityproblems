var PaginationCtrl = function ($scope)
{
    "use strict";
    $scope.maxSize = 5;
    $scope.pageChanged = function(page, as_get_parameter)
    {
        as_get_parameter = typeof as_get_parameter !== 'undefined' ? as_get_parameter : false;
        if(as_get_parameter)
            window.location.assign(window.location.pathname.toString()+"?page="+page);
        var currLink = window.location.pathname.toString();
        currLink = currLink.split(/\d+/)[0];
        if (page!=1)
        currLink+=page+'/';
        window.location.assign(currLink+window.location.search);
    };
};
PaginationCtrl.$inject = ['$scope'];