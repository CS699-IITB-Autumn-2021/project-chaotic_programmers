var studentCompanionApp = angular.module('studentCompanionApp', ['ui.router']);

studentCompanionApp.config(function($stateProvider, $urlRouterProvider) {
    
    $urlRouterProvider.otherwise('/home');
    
    $stateProvider
        
        // HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
            url: '/home',
            templateUrl: 'views/home.html'
        })

        .state('friends', {
            url: '/friends',
            templateUrl: 'views/friends.html'
        })

        .state('leaderboard', {
            url: '/leaderboard',
            templateUrl: 'views/leaderboard.html'
        })

        .state('flashcards', {
            url: '/flashcards',
            templateUrl: 'views/flashcards.html'
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

