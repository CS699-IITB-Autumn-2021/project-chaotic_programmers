var studentCompanionApp = angular.module('studentCompanionApp');
studentCompanionApp.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl('http://localhost:8000/api/');
    stored = localStorage.getItem('token');
    console.log('stored is', stored)
    if (stored) {
        stored_json = JSON.parse(stored)
        token = stored_json.token
        value = "Token " + token
        RestangularProvider.setDefaultHeaders({ 'Authorization': value });
    }

});
/**
 * Facilitates backend and frontend communication
 */
studentCompanionApp.factory('apiService', ['Restangular', function(Restangular) {



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
        fetchCardsofDeck: fetchCardsofDeck,
        loginUser: loginUser,
        registerUser: registerUser,
        logoutUser: logoutUser,
        fetchTodaysCardsofDeck: fetchTodaysCardsofDeck,
        SaveStartCard: SaveStartCard,
        SaveFinishCard: SaveFinishCard,
        deleteCard: deleteCard,
        shareDeckToFriend: shareDeckToFriend,
        EditCard: EditCard,
    };


    /**
     * Useful for getting all models when testing
     * @returns {list} All models
     */
    function getTestModels() {
        return Restangular.all('test').getList();
    }


    /**
     * Useful for getting specific models when testing
     * @param {number} id Specific id
     * @returns {list} Specific model
     */
    function getTestModel(id) {
        return Restangular.one('test', id).get();
    }

    /**
     * Gets all deck names
     * @returns {list} Deck names
     */
    function getDeckNames() {
        return Restangular.all('decks').getList();
    }

    /**
     * Gets currently logged in user
     * @returns {list} Logged in User details
     */
    function getCurrentUser() {
        return Restangular.one('get_logged_in_user').get()
    }

    /**
     * Gets user details    
     * @param {params} id Dictionary of User id
     * @returns {list} Specific User Details
     */
    function getUserDetails(params) {
        return Restangular.one('user').customGET("", params)
    }

    /**
     * Sends details of new friend to add it as friend
     * @param {params} id Dictionary of User id and friend id
     * @returns {list} Status of adding friend
     */
    function addFriend(params) {
        return Restangular.one('friends').customPOST(params, 'new/')
    }

    /**
     * Gets list of friends
     * @param {params} id Dictionary of User id
     * @returns {list} List of Friends
     */
    function getFriends(params) {
        return Restangular.one('friends').customGET("list", {})
    }

    /**
     * Gets leaderboard details in provided sorted order
     * @param {params} id Dictionary of ordering requirements
     * @returns {list} Leaderboard details
     */
    function getLeaderboard(params) {
        return Restangular.one('leaderboard').customGET("", params)
    }

    /**
     * Sends deck name to back end to create a new deck
     * @param {params} id Dictionary of deckname
     * @returns {list} Status of creating new deck
     */
    function createDeck(params) {
        return Restangular.one('decks').customPOST(params, "new/")
    }

    /**
     * Sends card details to backend to create new flashcard and save in database
     * @param {params} id Dictionary of card title, question and answer
     * @returns {list} Sattus of creating flashcard
     */
    function createCard(params) {
        return Restangular.one('card').customPOST(params, "new/")
    }

    /**
     * Sends card id and deck id to save start time
     * @param {params} id Dictionary of cardid ,deckid
     * @returns {list} Status of saving start time
     */
    function SaveStartCard(params) {
        return Restangular.one('card').customPOST(params, "savestart/")
    }

    /**
     * Sends card id and deck id to calculate total time taken and also calculate next scheduled time
     * @param {params} id Dictionary of cardid, deckid and difficulty level
     * @returns {list} Status of scheduling card
     */
    function SaveFinishCard(params) {
        return Restangular.one('card').customPOST(params, "savefinish/")
    }

    /**
     * Sends deck id to backend to delete deck
     * @param {params} id Dictionary of cardid
     * @returns {list} Status of card deletion
     */
    function deleteCard(params) {
        return Restangular.one('card').customPOST(params, "delete/")
    }

    /**
     * Sends new  card info to backend for updation
     * @param {params} id Dictionary of cardid and new card details
     * @returns {list} status of edit card
     */
    function EditCard(params) {
        return Restangular.one('card').customPOST(params, "edit/")
    }

    /**
     *  Fetches cards of a specific deck
     * @param {params} id Dictionary of deck id
     * @returns {list} Cards of specific deck
     */
    function fetchCardsofDeck(params) {
        return Restangular.one('card').customGET("", params);
    }

    /**
     * Sends deck id to get cards to be revised today
     * @param {params} id Dictionary of deck id
     * @returns {list}
     */
    function fetchTodaysCardsofDeck(params) {
        return Restangular.one('card').customGET("revise/", params);
    }

    /**
     * Redicts so that user is logged in
     * @param {params} id Dictionary of user details
     * @returns {list} Status of login
     */
    function loginUser(params) {
        return Restangular.one('login/').customPOST(params, "")
    }

    /**
     * Send new user details to be saved
     * @param {params} id Dictionary of new user details
     * @returns {list} Status of Registration of user
     */
    function registerUser(params) {
        return Restangular.one('register/').customPOST(params, "")
    }

    /**
     * Asks to log out user
     * @returns {list} Status of logout
     */
    function logoutUser() {
        return Restangular.one('logout/').customPOST("", "")
    }

    /**
     * Sends deck id and friend id to whom the deck is to be shared with
     * @param {params} id Dictionary of odeck id and friend id
     * @returns {list} Status of sharing of cards
     */
    function shareDeckToFriend(params) {
        return Restangular.one('sharedeck/').customPOST(params, '')
    }


    return service;

}]);