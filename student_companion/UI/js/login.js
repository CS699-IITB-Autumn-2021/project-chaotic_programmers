var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('loginCtrl', ['$scope', 'apiService', '$uibModal', '$window', '$state',function($scope, apiService, $uibModal, $window, $state) {
        
    $scope.checkIfLoggedIn = function(){
        storedData = localStorage.getItem('token');
        data = JSON.parse(storedData)
        if(data && data.token){
            $state.go('profile.home')
        }
    }

    $scope.login = function(){
        params = {
            username: $scope.userName,
            password: $scope.password
        }

        apiService.loginUser(params).then(function(response) {
            userData = JSON.stringify(response);
            localStorage.setItem('token', userData);
            $window.location.reload();
          }, function(response) {
            toastr.error("Try with Different username/password", 'Login Failed!');
          });

    }

    $scope.checkIfLoggedIn()
}])