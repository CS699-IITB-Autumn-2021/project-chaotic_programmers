var studentCompanionApp = angular.module('studentCompanionApp');


studentCompanionApp.directive('profile', function() {
    return {
        templateUrl: 'views/profile.html'
    };
});


studentCompanionApp.directive('login', function() {
    return {
        templateUrl: 'views/login/index.html'
    };
});