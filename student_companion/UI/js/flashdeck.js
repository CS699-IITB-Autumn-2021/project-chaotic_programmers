var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('flashdeckCtrl', ['$scope', 'apiService', '$uibModal', '$state', function($scope, apiService, $uibModal, $state) {

    $scope.saveDeck = function() {
        custom_required = 0
        const deck_ids = []
        if ($scope.custom_selected) {
            custom_required = 1
            $scope.decks.forEach(function(eachdeck) {
                if (eachdeck.selected) {
                    if (eachdeck != '') {
                        deck_ids.push(eachdeck.id)
                    }
                }
            });
            console.log(deck_ids);
        }
        var params = {
            title: $scope.deckName,
            custom_required: custom_required,
            deck_ids: deck_ids
        }
        apiService.createDeck(params).then(function(response) {
            toastr.success("New Deck Created", 'Success');
            $scope.getDecks();
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

    $scope.shareDeck = function(deck_id) {
        console.log('here at parent')
        $scope.open("lg", deck_id)
    }

    $scope.open = function(size, deck_id) {


        var modalInstance = $uibModal.open({
            animation: false,
            templateUrl: 'share_deck.html',
            controller: 'shareDeckCtrl',
            size: size,
            resolve: {
                deck: function() {
                    return deck_id;
                },
            }
        });

    };

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
            for (var i = 0; i < $scope.flashcards.length; i++) {
                date_time_scheduled_at = $scope.flashcards[i]["next_scheduled_at"];
                date_scheduled_at = date_time_scheduled_at.split("T")[0];
                $scope.year_scheduled_at = date_scheduled_at.split("-")[0];
                switch (date_scheduled_at.split("-")[1]) {
                    case "01":
                        // code block
                        $scope.month_scheduled_at = " January ";
                        break;
                    case "02":
                        $scope.month_scheduled_at = " February ";
                        break;
                    case "03":
                        $scope.month_scheduled_at = " March ";
                        break;
                    case "04":
                        $scope.month_scheduled_at = " April ";
                        break;
                    case "05":
                        $scope.month_scheduled_at = " May ";
                        break;
                    case "06":
                        $scope.month_scheduled_at = " June ";
                        break;
                    case "07":
                        $scope.month_scheduled_at = " July ";
                        break;
                    case "08":
                        $scope.month_scheduled_at = " August ";
                        break;
                    case "09":
                        $scope.month_scheduled_at = " September ";
                        break;
                    case "10":
                        $scope.month_scheduled_at = " October ";
                        break;
                    case "11":
                        $scope.month_scheduled_at = " November ";
                        break;
                    case "12":
                        $scope.month_scheduled_at = " December ";
                        break;
                    default:
                        // code block
                }
                $scope.day_scheduled_at = date_scheduled_at.split("-")[2];

            }
        });
    }
    $scope.getCard = function(flashcard_id) {
        for (var i = 0; i < $scope.flashcards.length; i++) {
            if ($scope.flashcards[i]["id"] == flashcard_id) {
                $scope.currEditFlashcardid = flashcard_id;
                $scope.currEditFlashcardTitle = $scope.flashcards[i]["title"];
                $scope.currEditFlashcardQuestion = $scope.flashcards[i]["question"];
                $scope.currEditFlashcardAnswer = $scope.flashcards[i]["answer"];
                $scope.editflashcardTitle = $scope.currEditFlashcardTitle;
                $scope.editflashcardQuestion = $scope.currEditFlashcardQuestion;
                $scope.editflashcardAnswer = $scope.currEditFlashcardAnswer;
            }
        }
    }
    $scope.editCard = function() {
        if (typeof $scope.editflashcardTitle == 'undefined') {
            flashtitle = $scope.currEditFlashcardTitle;
        } else {
            flashtitle = $scope.editflashcardTitle;
        }
        if (typeof $scope.editflashcardQuestion == 'undefined') {
            flashquestion = $scope.currEditFlashcardQuestion;
        } else {
            flashquestion = $scope.editflashcardQuestion;
        }
        if (typeof $scope.editflashcardAnswer == 'undefined') {
            flashanswer = $scope.currEditFlashcardAnswer;
        } else {
            flashanswer = $scope.editflashcardAnswer;
        }

        params = {
            card_id: $scope.currEditFlashcardid,
            title: flashtitle,
            question: flashquestion,
            answer: flashanswer
        }
        console.log($scope.currEditFlashcardid);
        apiService.EditCard(params).then(function(response) {
            $scope.getCards()
            toastr.success("FlashCard Edited", 'Success');
        }, function(response) {
            toastr.error("Please try again later.", 'Failed to edit card');
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
            toastr.error("Please try again later.", 'Failed to delete card');
        });
    }
    $scope.getCards()

}])


studentCompanionApp.controller('flashcardShowCtrl', ['$scope', 'apiService', '$uibModal', '$state', '$stateParams', function($scope, apiService, $uibModal, $state, $stateParams) {

    console.log($stateParams)
}])



studentCompanionApp.controller('shareDeckCtrl', ['$scope', 'apiService', '$modalInstance', 'deck', '$window', function($scope, apiService, $modalInstance, deck, $window) {


    console.log('form share')
    $scope.deckId = deck


    $scope.ok = function() {
        $modalInstance.dismiss('cancel');
        $scope.share()
    };

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

    apiService.getFriends().then(function(response) {
        $scope.friends = response;
    });

    $scope.share = function() {
        var params = {
            friend_id: $scope.friend_id,
            deck_id: $scope.deckId
        }
        console.log(params)
        apiService.shareDeckToFriend(params).then(function(response) {
            toastr.success("Added to friend list", 'Success');
        }, function(response) {
            toastr.error("No such user/ friend already added", 'Failed to add friend');
        });

    }

}]);