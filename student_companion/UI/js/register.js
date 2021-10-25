var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('registerCtrl', ['$scope', 'apiService', '$uibModal','$state', function($scope, apiService, $uibModal, $state) {
        
    $scope.checkIfLoggedIn = function(){
        storedData = localStorage.getItem('token');
        data = JSON.parse(storedData)
        if(data && data.token){
            $state.go('profile.home')
        }
    }

    $scope.register = function(){
        params = {
            username: $scope.userName,
            password: $scope.password,
            password2: $scope.confirmPassword,
            email: $scope.emailId,
            first_name: $scope.firstName,
            last_name: $scope.lastName
        }

        apiService.registerUser(params).then(function(response) {
            toastr.success("You were registered", 'Success');
            $state.go('public.login')
          }, function(response) {
            toastr.error("Please check the data entered!!", 'Registration Failed!');
          });
    }

    $scope.checkIfLoggedIn()
}])