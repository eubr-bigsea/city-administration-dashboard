(function () {
    'use strict';

    angular.module("TPAnalytics.directives")
        .directive('visualizacaoBilhetagem', function () {
            return {
                restrict: "E",
                templateUrl: "../js/directives/visualizacao_bilhetagem.html"
            };
        });
}());
