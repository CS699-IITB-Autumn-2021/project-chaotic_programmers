var studentCompanionApp = angular.module('studentCompanionApp', ['ui.router', 'restangular']);



studentCompanionApp.controller('flashcardCtrl', ['$scope', 'apiService', function($scope, apiService) {

    console.log('load aavuthu')

    // get examples by using exampleService
    // apiService.getTestModels().then(function(response) {
    //     $scope.examples = response;
    // });

    // // get example with given id by using exampleService
    // apiService.getTestModel('1').then(function(response) {
    //     $scope.example = response;
    // });

    apiService.getDeckNames().then(function(response) {
        $scope.decks = response;
    });

}])