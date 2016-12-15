(function () {
    'use strict';

    angular.module("TPAnalytics")
        .factory('ranking_de_atrasos', ['$http', 'api_link_service', function ($http, api_link_service){
            return {
                getData: function(date){
                    if (date == undefined) {
                        return $http.get(api_link_service.getAPI() + "api/m0/delay_ranking")
                            .success(function(data){
                            })
                            .error(function(err){
                                alert("Desculpe-nos ocorreu um erro imprevisto. Atualize a página");
                            });
                    }else {
                        return $http.get(api_link_service.getAPI() + "api/m0/delay_ranking/" + date)
                            .success(function(data){
                            })
                            .error(function(err){
                                alert("Desculpe-nos ocorreu um erro imprevisto. Atualize a página");
                            });
                    }
                }
            };
        }]);

}());

