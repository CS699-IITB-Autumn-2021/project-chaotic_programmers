var studentCompanionApp = angular.module('studentCompanionApp');

studentCompanionApp.config(function($stateProvider, $urlRouterProvider) {
    
    $urlRouterProvider.otherwise('/home');
    
    $stateProvider
        
        // HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
            url: '/home',
            templateUrl: 'views/home.html',
            controller: 'indexCtrl',
        })

        .state('friends', {
            url: '/friends',
            templateUrl: 'views/friends.html',
            controller: 'friendsCtrl',
        })

        .state('leaderboard', {
            url: '/leaderboard',
            templateUrl: 'views/leaderboard.html',
            controller: 'leaderboardCtrl',
        })

        .state('flashcards', {
            url: '/flashcards',
            templateUrl: 'views/flashcards.html',
            controller: 'flashcardCtrl',
        })

        .state('flashcards.view', {
            url: '/view',
            templateUrl: 'views/flashcards_view.html'
        })

        .state('flashcards.new', {
            url: '/new',
            templateUrl: 'views/flashcards_new.html'
        })

        
        
});

