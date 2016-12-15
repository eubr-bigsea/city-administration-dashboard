(function () {
    'use strict';

    angular.module("TPAnalytics.directives")
        .directive('visualizacaoMonitoramento', function () {
            return {
                restrict: "E",
                templateUrl: "../js/directives/visualizacao_monitoramento.html"
            };
        });
}());

