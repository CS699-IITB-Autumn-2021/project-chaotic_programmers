var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('registerCtrl', ['$scope', 'apiService', '$uibModal','$state', function($scope, apiService, $uibModal, $state) {
        
    $scope.validations = {
        username: true,
        email: true
    }
    
    $scope.checkIfLoggedIn = function(){
        storedData = localStorage.getItem('token');
        data = JSON.parse(storedData)
        if(data && data.token){
            $state.go('profile.home')
        }
    }


    $scope.searchUser = function(key, value){
        var params = {
            key: key,
            value: value
        }

        console.log(params, $scope.searchFilter)
        apiService.getUserDetails(params).then(function(response) {
            $scope.validations[key] = false
          }, function(response) {
            $scope.validations[key] = true
          });

        

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
            console.log(response)
            var error_msg = ""
            Object.keys(response.data).forEach(function (key) { 
                var value = response.data[key]
                
                error_msg += (key+ " : ") 
                error_msg += value.join()
                error_msg += ";\n"
            })

            
              


              
            toastr.error(error_msg, 'Registration Failed!');
          });
    }

    $scope.checkIfLoggedIn()
}])