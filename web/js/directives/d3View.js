(function () {
    'use strict';

    angular.module("TPAnalytics.directives")
        .directive('d3View', function () {
            return {
                restrict: "E",
                templateUrl: "../js/directives/d3View.html"
            };
        });
}());
