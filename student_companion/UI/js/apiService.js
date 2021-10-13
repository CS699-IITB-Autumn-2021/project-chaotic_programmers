var studentCompanionApp = angular.module('studentCompanionApp');
studentCompanionApp.config(function(RestangularProvider) {
    RestangularProvider.setBaseUrl('http://localhost:8000/api/');
 });

 studentCompanionApp.factory('apiService', ['Restangular', function(Restangular){

    // this is service object with list of methods in it
    // this object will be used by controller


    var service = {
        getTestModels: getTestModels,
        getTestModel: getTestModel
    };

    // get examples from server by using Restangular
    function getTestModels(){
        return Restangular.all('test').getList();
    }

    // get example with given id from server by using Restangular
    function getTestModel(id){
        return Restangular.one('test', id).get();
    }

    return service;

}]);