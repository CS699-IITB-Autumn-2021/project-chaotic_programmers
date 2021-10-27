var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('friendsCtrl', ['$scope', 'apiService', '$uibModal', function($scope, apiService, $uibModal) {

    $scope.searchOptions = ['username', 'email']
    $scope.searchFilter = $scope.searchOptions[0]

    $scope.searchFilter = ""
    $scope.searchQuery = ""
    $scope.searchStatusSuccess = true


    /**
     * Get friends of user
     */
    apiService.getFriends().then(function(response) {
        $scope.friends = response;

    });



    /**
     * Search for friends
     */
    $scope.searchFriend = function() {
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


    /**
     * Opening Add friend popup
     */
    $scope.open = function(size, resp) {
        var modalInstance = $uibModal.open({
            animation: false,
            templateUrl: 'add_friend_popup.html',
            controller: 'addFriendCtrl',
            size: size,
            resolve: {
                friend: function() {
                    return resp;
                },
                currentUser: function() {
                    return $scope.user
                },
            }
        });

    };




}])

// studentCompanionApp.controller('ModalInstanceCtrl', function ($scope, $modalInstance, friend, currentUser) {
studentCompanionApp.controller('addFriendCtrl', ['$scope', 'apiService', '$modalInstance', 'friend', 'currentUser', '$window', function($scope, apiService, $modalInstance, friend, currentUser, $window) {


    $scope.friend = friend
    $scope.currentUser = currentUser


    /**
     * Clicking on okay to add friends
     */
    $scope.ok = function() {
        $modalInstance.dismiss('cancel');
        $scope.add()
    };

    /**
     * Clicking cancel in add friend popup
     */
    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

    /**
     * Adding friend
     */
    $scope.add = function() {
        var params = {
            friend_id: $scope.friend.id
        }
        apiService.addFriend(params).then(function(response) {
            toastr.success("Added to friend list", 'Success');
            $window.location.reload();
        }, function(response) {
            toastr.error("No such user/ friend already added", 'Failed to add friend');
        });

    }

}]);