var studentCompanionApp = angular.module('studentCompanionApp');


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

    $scope.reloadDecks = function() {
        apiService.getDeckNames().then(function(response) {
            $scope.decks = response;
        });
    }
    $scope.saveDeck = function() {
        var params = {
            title: $scope.new_deck_name,
            owner_id: 1
        }
        apiService.createDeck(params).then(function(response) {
            toastr.success("New Deck Created", 'Success');
            $scope.reloadDecks();
        }, function(response) {
            toastr.error("Please try again later.", 'Failed to create deck');
        });
    }


    $scope.selectedDeckFromDropDown = function(index) {
        console.log($scope.decks[index]);
        $scope.curr_deck_id = $scope.decks[index].id;
        var params = {
            owner_id: 1,
            flash_deck_id: $scope.curr_deck_id
        }
        apiService.fetchCardsofDeck(params).then(function(response) {
            $scope.cardsofDeck = response;
            $scope.size_of_today_deck = $scope.cardsofDeck.length;
            console.log($scope.size_of_today_deck)
        });
        $scope.current_card_index = 0;
        $scope.cards_revised_percentage = 0;
        console.log($scope.current_card_index);
    }

    $scope.newFlashCard = function() {
        var params = {
            title: $scope.new_fcard_title,
            question: $scope.new_fcard_front,
            answer: $scope.new_fcard_front,
            owner_id: 1,
            flash_deck_id: $scope.curr_deck_id
        }
        apiService.createCard(params).then(function(response) {
            toastr.success("New Card Created", 'Success');
        }, function(response) {
            toastr.error("Please try again later.", 'Failed to create flashcard');
        });
    }
    $scope.shownextCard = function() {
        $scope.current_card_index = $scope.current_card_index + 1;
        $scope.cards_revised_percentage = $scope.current_card_index / $scope.size_of_today_deck * 100;
        console.log($scope.cards_revised_percentage)
    }
}])