var studentCompanionApp = angular.module('studentCompanionApp');

console.log('from directive')
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
  