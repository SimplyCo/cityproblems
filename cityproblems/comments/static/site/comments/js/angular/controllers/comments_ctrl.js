function commentsCtrl($scope, $http)
{
    "use strict";
    $scope.loadComments = function()
    {
        $http.get($scope.getCommentsLink)
        .success(function(data, status, headers, config)
        {
            if ("Error" in data)
                $scope.alerts.push({type: 'danger', msg: data["Error"]});
            else
            {
                $scope.comments=data.Comments;
                $scope.isLoadComplete=true;
            }
        })
        .error(function(data, status, headers, config)
        {
            $scope.alerts.push({type: 'danger', msg: "Error get comments"});
        });
    };

    $scope.remove = function (comment)
    {
        if (confirm('Remove this thread?'))
        {
            $http.post($scope.rmLink, {id: comment.id})
                .success(function(data, status, headers, config)
                {
                    if ("Error" in data)
                        $scope.alerts.push({type: 'danger', msg: data["Error"]});
                    else
                        window.location.reload();
                })
                .error(function(data, status, headers, config)
                {
                    $scope.alerts.push({type: 'danger', msg: "Error while send comment"});
                });
        }
    };

    $scope.sendchangedcomment = function (comment)
    {
        $http.post($scope.changesLink, {id: comment.id, text: comment.data.content})
            .success(function(data, status, headers, config)
            {
                if ("Error" in data)
                    $scope.alerts.push({type: 'danger', msg: data["Error"]});
                else
                {
                    comment.showEdit=false;
                    comment.data.isEditMe=true;
                }
            })
            .error(function(data, status, headers, config)
            {
                $scope.alerts.push({type: 'danger', msg: "Error while send comment"});
            });
    };


    $scope.sendnewcomment = function (parent)
    {
        var text;
        var parentID;
        if(!parent)
        {
            parentID='0';
            text=$scope.newComment.text;
        }
        else
        {
            parentID = parent.id;
            text = parent.reply;
        }
        $http.post($scope.sendUrl, {parentID: parentID, text: text})
            .success(function(data, status, headers, config)
            {
                if ("Error" in data)
                    $scope.alerts.push({type: 'danger', msg: data["Error"]});
                else
                {
                    if(!parent)
                    {
                        window.location.reload();
                    }
                    else
                    {
                        var comment={data: {username: $scope.userName, createDateTime: new Date(), content: text, avatar: data.avatar}, id: data.id, children:[]};
                        if(!parent.children)
                            parent.children=[];
                        parent.children.push(comment);
                        parent.showReply=false;
                        parent.reply="";
                    }
                }
            })
            .error(function(data, status, headers, config)
            {
//                 document.write(data);
                $scope.alerts.push({type: 'danger', msg: 'Error while send comment'});
            });
    };
}
commentsCtrl.$inject = ['$scope', "$http"];

function alertsCtrl($scope)
{
    "use strict";
    $scope.alerts = [];
    $scope.closeAlert = function(index)
    {
        $scope.alerts.splice(index, 1);
    };
}
alertsCtrl.$inject = ['$scope'];
