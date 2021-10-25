var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('flashdeckCtrl', ['$scope', 'apiService', '$uibModal', '$state', function($scope, apiService, $uibModal, $state) {

    $scope.saveDeck = function() {
        var params = {
            title: $scope.deckName
        }
        apiService.createDeck(params).then(function(response) {
            toastr.success("New Deck Created", 'Success');
            $scope.getDecks()
                // $scope.reloadDecks();
        }, function(response) {
            toastr.error("Please try again later.", 'Failed to create deck');
        });
    }

    $scope.getDecks = function() {
        apiService.getDeckNames().then(function(response) {
            $scope.decks = response;
        });
    }

    $scope.viewDeck = function(deck_id) {
        $state.go("profile.flashdeck_show", { id: deck_id })
    }

    $scope.getDecks()



}])


studentCompanionApp.controller('flashdeckShowCtrl', ['$scope', 'apiService', '$uibModal', '$state', '$stateParams', function($scope, apiService, $uibModal, $state, $stateParams) {
    console.log('I am here')
    console.log($stateParams)
    $scope.flashDeckId = $stateParams.id


    $scope.saveCard = function() {
        var params = {
            title: $scope.flashcardTitle,
            question: $scope.flashcardQuestion,
            answer: $scope.flashcardAnswer,
            deck_id: $scope.flashDeckId
        }
        apiService.createCard(params).then(function(response) {
            toastr.success("New Flashcard Created", 'Success');
            $scope.getCards()
        }, function(response) {
            toastr.error("Please try again later.", 'Failed to create card');
        });
    }

    $scope.getCards = function() {
        params = {
            deck_id: $scope.flashDeckId
        }

        apiService.fetchCardsofDeck(params).then(function(response) {
            $scope.flashcards = response;
        });
    }

    $scope.viewCard = function(flashcard_id) {
        $state.go("profile.flashcard_show", { flashcard_id: flashcard_id })
    }
    $scope.delCard = function(flashcard_id) {
        params = {
            card_id: flashcard_id
        }
        apiService.deleteCard(params).then(function(response) {
            $scope.getCards()
            toastr.success("FlashCard deleted", 'Success');
        }, function(response) {
            toastr.error("Please try again later.", 'Failed to create card');
        });
    }
    $scope.getCards()

}])


studentCompanionApp.controller('flashcardShowCtrl', ['$scope', 'apiService', '$uibModal', '$state', '$stateParams', function($scope, apiService, $uibModal, $state, $stateParams) {

    console.log($stateParams)
}])