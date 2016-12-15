(function () {
    'use strict';

    angular.module("TPAnalytics")
        .factory('equiv_overtime', ['$http', 'api_link_service', function($http, api_link_service) {
            return {
                getData: function(feature, startDate, endDate){
                    return $http.get(api_link_service.getAPI() +'api/m0/time_stocking/' + feature + '/' + startDate + '/' + endDate)
                        .success(function(data){
                        })
                        .error(function(err){
                            alert("Desculpe-nos ocorreu um erro imprevisto. Atualize a página");
                        });
                }
            };
        }]);

}());

