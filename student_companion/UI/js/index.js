var studentCompanionApp = angular.module('studentCompanionApp', ['ui.router', 'restangular', 'ngAnimate','ui.bootstrap']);

console.log('from index')

studentCompanionApp.controller('indexCtrl', ['$scope', 'apiService', function($scope, apiService) {

   

}])


studentCompanionApp.controller('mainCtrl', ['$scope', 'apiService', function($scope, apiService) {

    console.log("from main ctr")
    // apiService.getCurrentUser().then(function(response) {
    //     $scope.user = response;
    // });
    $scope.loggedIn = false

}])