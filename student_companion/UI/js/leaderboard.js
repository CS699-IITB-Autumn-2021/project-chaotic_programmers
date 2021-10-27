var studentCompanionApp = angular.module('studentCompanionApp');



studentCompanionApp.controller('leaderboardCtrl', ['$scope', 'apiService', '$uibModal', function($scope, apiService, $uibModal) {

    $scope.periodOptions = ['Last 1 Month', 'Last 7 Days', 'Last 1 day']
    $scope.rankCriteria = ['Cards Revised', 'Time Spent']

    $scope.timePeriod = $scope.periodOptions[0]
    $scope.criteria = $scope.rankCriteria[0]

    /**
     * Get Leaderboard Data
     */
    $scope.getData = function() {
        var params = {
            period: $scope.timePeriod,
            criteria: $scope.criteria
        }

        apiService.getLeaderboard(params).then(function(response) {
            $scope.leaderboard = response;
        });
    }

    $scope.getData()
}])