var studentCompanionApp = angular.module('studentCompanionApp');

console.log('from friends')
studentCompanionApp.directive('searchFriends', function() {
    return {
      templateUrl: 'view/flahscards_view.html'
    };
  });
  