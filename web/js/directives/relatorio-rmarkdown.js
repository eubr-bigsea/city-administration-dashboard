(function () {
    'use strict';

    angular.module("TPAnalytics.directives")
        .directive('relatorioRmarkdown', function () {
            return {
                restrict: "E",
                templateUrl: "../js/directives/relatorio-rmarkdown.html",
                link: function () {
                      $('.r').remove();
                }
            };
        });
}());
