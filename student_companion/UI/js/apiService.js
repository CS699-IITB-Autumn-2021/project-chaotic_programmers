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

    function getCurrentUser(){
        return Restangular.one('get_logged_in_user').get()
    }

    function getUserDetails(params){
        return Restangular.one('user').customGET("", params)
    }

    function addFriend(params){
        return Restangular.one('friends').customPOST(params, 'new/')
    }

    function getFriends(params){
        return Restangular.one('friends').customGET("list", {})
    }

    
    return service;

}]);