var studentCompanionApp = angular.module('studentCompanionApp');


studentCompanionApp.controller('flashcardCtrl', ['$scope', 'apiService', function($scope, apiService) {
    $scope.cardVisible = false;
    $scope.backVisible = false;
    $scope.cardFlipped = false
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
    $scope.CardShow = function() {
        $scope.cardVisible = true;
        console.log('Show card');

    }

    $scope.CardHide = function() {
        $scope.cardVisible = false;
    }

    $scope.BackShow = function() {
        $scope.backVisible = true;
        console.log("Show backside of card");
    }

    $scope.BackHide = function() {
        $scope.backVisible = false;
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
            deck_id: $scope.curr_deck_id
        }
        apiService.fetchCardsofDeck(params).then(function(response) {
            $scope.cardsofDeck = response;
            $scope.size_of_today_deck = $scope.cardsofDeck.length;

            $scope.current_card_index = 0;
            $scope.cards_revised_percentage = 0;
            $scope.cards_revised_percentage = $scope.current_card_index / $scope.size_of_today_deck * 100;
            if ($scope.size_of_today_deck && $scope.size_of_today_deck <= 0) {
                $scope.cards_revised_percentage = 100
                toastr.info("You are all caught up..No cards to revise in this deck", 'Info');
                $scope.cardVisible = false;
            }
            console.log($scope.size_of_today_deck)
        });
        console.log($scope.current_card_index);
    }



    $scope.selectedDeckForRevision = function(index) {
        console.log($scope.decks[index]);
        $scope.curr_deck_id = $scope.decks[index].id;
        var params = {
            deck_id: $scope.curr_deck_id
        }
        apiService.fetchTodaysCardsofDeck(params).then(function(response) {
            $scope.cardsofDeck = response;
            $scope.size_of_today_deck = $scope.cardsofDeck.length;
            $scope.current_card_index = 0;
            $scope.cards_revised_percentage = 0;
            $scope.cards_revised_percentage = $scope.current_card_index / $scope.size_of_today_deck * 100;
            // console.log($scope.cardsofDeck[0].id)
            if ($scope.size_of_today_deck != 0) {
                $scope.StartCard($scope.cardsofDeck[0].id);
            } else {
                $scope.CardHide();
                $scope.BackHide();
                toastr.success("No cards for revision, come back later!", 'Success');
            }
        });
        console.log($scope.current_card_index);
    }
    $scope.StartCard = function(card_id) {
        console.log("Flashcard id: " + card_id)
        var params = {
            flashcard_id: card_id
        }
        apiService.SaveStartCard(params).then(function(response) {
            console.log("Saved start datetime in next_scheduled_date");
        }, function(response) {
            console.log("Failed to save the start datetime in next_scheduled_date");
        });
        console.log($scope.current_card_index);
    }
    $scope.FinishCard = function(card_id, diff) {
        console.log("Flashcard id: " + card_id)
        var params = {
            flashcard_id: card_id,
            difficulty: diff,
        }
        apiService.SaveFinishCard(params).then(function(response) {
            console.log("Saved end datetime in next_scheduled_date");
        }, function(response) {
            console.log("Failed to save the end datetime in next_scheduled_date");
        });
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
    $scope.shownextCard = function(difficulty) {
        $scope.FinishCard($scope.cardsofDeck[$scope.current_card_index].id, difficulty);
        $scope.current_card_index = $scope.current_card_index + 1;
        $scope.cards_revised_percentage = Math.floor($scope.current_card_index / $scope.size_of_today_deck * 100);
        console.log($scope.cards_revised_percentage)
        if ($scope.size_of_today_deck == $scope.current_card_index) {
            $scope.CardHide();
            $scope.BackHide();
            toastr.success("Finished today's revision for this deck", 'Success');
        } else {
            $scope.StartCard($scope.cardsofDeck[$scope.current_card_index].id)
        }
    }
}])