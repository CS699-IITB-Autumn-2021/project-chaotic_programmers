var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('profileCtrl', ['$scope', 'apiService', '$uibModal', '$window', '$state', function($scope, apiService, $uibModal, $window, $state) {


    /**
     * Check if user has logged in
     */
    $scope.checkIfLoggedIn = function() {
        storedData = localStorage.getItem('token');
        data = JSON.parse(storedData)
        if (!data || !data.token) {
            $state.go('public.login')
        } else {
            userDetails = {
                firstName: data.first_name,
                lastName: data.last_name
            }
            $scope.user = userDetails
        }
    }


    /**
     * Log out the user
     */
    $scope.logout = function() {
        apiService.logoutUser().then(function(response) {
            localStorage.removeItem('token');
            $window.location.reload();
        }, function(response) {
            toastr.error("Try again later", 'Logout Failed!');
        });
    }

    $scope.checkIfLoggedIn()
}])