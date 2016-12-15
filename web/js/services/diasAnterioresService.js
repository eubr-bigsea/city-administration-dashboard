(function () {
    'use strict';

    angular.module("TPAnalytics")
        .factory('dias_anteriores', ['$http', 'api_link_service', function($http, api_link_service){

            return {
                getData: function(rota, dataViagem){
                    return $http.get(api_link_service.getAPI() + "api/m0/get_travels_before_yesterday/" + dataViagem + "/" + rota)
                        .success(function(data){
                        })
                        .error(function(err){
                            alert("Desculpe-nos ocorreu um erro imprevisto. Atualize a página");
                        });
                }
            };
        }]);

}());

