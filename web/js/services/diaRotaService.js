(function () {
    'use strict';

    angular.module("TPAnalytics")
        .factory('dia_rota', ['$http', 'api_link_service', function($http, api_link_service){

            return {
              getData: function(rota, dataViagem){
                  return $http.get(api_link_service.getAPI() + "api/m0/route_trips/" + dataViagem + "/" + rota)
                      .success(function(data){
                      })
                      .error(function(err){
                          alert("Desculpe-nos ocorreu um erro imprevisto. Atualize a página");
                      });
              }
            };
        }]);

}());

