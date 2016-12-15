(function () {
    'use strict';

    angular.module("TPAnalytics.controllers")
        .controller("MainController", ["$scope", "$rootScope", function($scope, $rootScope){
            $scope.appName = "Observatório do Transporte";

            $scope.currentPage = "index.conteudo.panorama";

            $scope.upperMenu = [
                {
                    name: "Panorama",
                    icon: "glyphicon glyphicon-home",
                    reference: "index.conteudo.panorama"
                },
                {
                    name: "Escala",
                    icon: "glyphicon glyphicon-time",
                    reference: "index.conteudo.graficosHorarios"
                }
                //,
                // {
                //     name: "Tendências",
                //     icon: "glyphicon glyphicon-stats",
                //     reference: "index.conteudo.tendencias"
                // },
                // {
                //     name: "Análises",
                //     icon: "glyphicon glyphicon-signal",
                //     reference: "index.conteudo.analises"
                // }
            ];

            $scope.graphics = false;
            $scope.toggleGraphics = function(item) {
                if(item.name == "Gráficos") {
                    $scope.graphics = !$scope.graphics;
                }
            };

            $scope.logOut = function() {
                $rootScope.currentUser = undefined;
            }

            $scope.changeCurrentPage = function(reference){
                $scope.currentPage = reference;
            }
        }]);
}());

