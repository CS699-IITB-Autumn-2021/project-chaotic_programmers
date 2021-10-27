var studentCompanionApp = angular.module('studentCompanionApp', ['ui.router', 'restangular', 'ngAnimate', 'ui.bootstrap']);


studentCompanionApp.controller('indexCtrl', ['$scope', 'apiService', function($scope, apiService) {



}])


studentCompanionApp.controller('mainCtrl', ['$scope', 'apiService', function($scope, apiService) {

    // apiService.getCurrentUser().then(function(response) {
    //     $scope.user = response;
    // });
    $scope.loggedIn = false

}])