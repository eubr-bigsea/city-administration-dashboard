(function () {
    'use strict';

    angular.module("TPAnalytics")
        .factory('loginService', ['$http', '$rootScope', 'api_link_service', function($http, $rootScope, api_link_service){
            return {
                checkAuth: function(username, password){
                    return $http.get(api_link_service.getAPI() + "api/m0/login/" + username + "/" + password)
                        .success(function(data){
                            if (data[0].usuario != "False"){
                                $rootScope.currentUser = username;

                                window.location = "#/index/conteudo/panorama";
                            } else {
                                $rootScope.currentUser = undefined;
                                alert("Usuário ou senha inválida, por favor se logue novamente!");
                            }
                        })
                        .error(function(err){
                            alert("Desculpe-nos ocorreu um erro imprevisto. Atualize a página");
                        });
                }

            };
        }]);

}());