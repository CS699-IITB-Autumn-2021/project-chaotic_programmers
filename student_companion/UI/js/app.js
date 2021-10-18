var studentCompanionApp = angular.module('studentCompanionApp');

deckName: ""

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

    $scope.saveDeck = function() {
        var params = {
            title: $scope.new_deck_name,
            owner_id: 1,
            created_at: '2021-10-10',
            updated_at: '2021-10-10'
        }
        apiService.createDeck(params).then(function(response) {
            toastr.success("New Deck Created", 'Success');
        }, function(response) {
            toastr.error("Please try again later.", 'Failed to create deck');
        });

    }


    $scope.selectedDeckFromDropDown = function() {

        deckName: $scope.deck_name

    }


}])