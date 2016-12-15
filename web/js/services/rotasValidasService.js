(function () {
    'use strict';

    angular.module("TPAnalytics")
        .factory('rotas_validas', ['$http', 'api_link_service', function($http, api_link_service){
            return {
                getData: function(){
                    return $http.get(api_link_service.getAPI() + "api/m0/valid_routes")
                        .success(function(data){
                        })
                        .error(function(err){
                            alert("Desculpe-nos ocorreu um erro imprevisto. Atualize a página");
                        });
                }
            };
        }]);

}());

