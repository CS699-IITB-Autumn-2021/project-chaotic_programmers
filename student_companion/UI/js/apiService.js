var studentCompanionApp = angular.module('studentCompanionApp');
studentCompanionApp.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl('http://localhost:8000/api/');
});

studentCompanionApp.factory('apiService', ['Restangular', function(Restangular) {

    // this is service object with list of methods in it
    // this object will be used by controller


    var service = {
        getTestModels: getTestModels,
        getTestModel: getTestModel,
        getDeckNames: getDeckNames,
        getCurrentUser: getCurrentUser,
        getUserDetails: getUserDetails,
        addFriend: addFriend,
        getFriends: getFriends,
        getLeaderboard: getLeaderboard,
        createDeck: createDeck,
        createCard: createCard,
    };

    // get examples from server by using Restangular
    function getTestModels() {
        return Restangular.all('test').getList();
    }

    // get example with given id from server by using Restangular
    function getTestModel(id) {
        return Restangular.one('test', id).get();
    }

    function getDeckNames() {
        return Restangular.all('decks').getList();
    }

    function getCurrentUser() {
        return Restangular.one('get_logged_in_user').get()
    }

    function getUserDetails(params) {
        return Restangular.one('user').customGET("", params)
    }

    function addFriend(params) {
        return Restangular.one('friends').customPOST(params, 'new/')
    }

    function getFriends(params) {
        return Restangular.one('friends').customGET("list", {})
    }

    function getLeaderboard(params) {
        return Restangular.one('leaderboard').customGET("", params)
    }

    function createDeck(params) {
        return Restangular.one('decks').customPOST(params, "new/")
    }

    function createCard(params) {
        return Restangular.one('card').customPOST(params, "new/")
    }

    return service;

}]);