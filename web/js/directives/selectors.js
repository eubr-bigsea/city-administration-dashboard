(function () {
    'use strict';

    angular.module("TPAnalytics.directives")
        .directive('selectors', function () {
            return {
                restrict: "E",
                templateUrl: "../js/directives/selectors.html"
            };
        });
}());
