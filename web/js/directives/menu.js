(function () {
    'use strict';

    angular.module("TPAnalytics.directives")
        .directive("menu", function(){
            return {
                restrict: "E",
                templateUrl: "../js/directives/menu.html"
            };
        });
}());

