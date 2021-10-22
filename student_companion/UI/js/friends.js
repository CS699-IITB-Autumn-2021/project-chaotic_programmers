var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('friendsCtrl', ['$scope', 'apiService', '$uibModal', function($scope, apiService, $uibModal) {

    $scope.searchOptions = ['username', 'email']
    console.log($scope.loggedIn)

    $scope.searchFilter = ""
    $scope.searchQuery = ""
    $scope.searchStatusSuccess = true
            
    apiService.getFriends().then(function(response) {
        $scope.friends = response;
        
        console.log(toastr)
    });

    

    $scope.searchFriend = function(){
        var params = {
            key: $scope.searchFilter,
            value: $scope.searchQuery
        }

        console.log(params, $scope.searchFilter)
        apiService.getUserDetails(params).then(function(response) {
            $scope.searchStatusSuccess = true
            $scope.friend = response
            $scope.open('lg', response)
          }, function(response) {
            toastr.error("Try with Different username/password", 'No such user found !');
          });

        

    }


    $scope.open = function (size, resp) {

        console.log('opend')
        
        var modalInstance = $uibModal.open({
            animation: false,
            templateUrl: 'add_friend_popup.html',
            controller: 'addFriendCtrl',
            size: size,
            resolve: {
                friend: function () {
                    return resp;
                },
                currentUser: function(){
                    return $scope.user
                },
            }
        });
    
    };

    
    
    
}])

// studentCompanionApp.controller('ModalInstanceCtrl', function ($scope, $modalInstance, friend, currentUser) {
studentCompanionApp.controller('addFriendCtrl', ['$scope', 'apiService', '$modalInstance', 'friend', 'currentUser', function($scope, apiService, $modalInstance, friend, currentUser) {

  
    $scope.friend = friend
    $scope.currentUser = currentUser
    console.log(friend)
    $scope.ok = function () {
        $modalInstance.dismiss('cancel');
        $scope.add()
    };
  
    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };

    $scope.add = function(){
        var params = {
            friend_id : $scope.friend.id
        }
        apiService.addFriend(params).then(function(response) {
            toastr.success("Added to friend list", 'Success');
          }, function(response) {
            toastr.error("Please try again later.", 'Failed to add friend');
          });

    }

  }]);