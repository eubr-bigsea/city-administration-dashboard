(function () {
    'use strict';

    // create the angular app
    angular.module("TPAnalytics", [
        'ui.router',
        'TPAnalytics.controllers',
        'TPAnalytics.directives',
        'ui.bootstrap',
        "uiSwitch",
        'ngSanitize',
        'ui.select',
        'ngLoadingSpinner',
        'nvd3',
        'rzModule'
    ]);

    // setup dependency injection
    angular.module('TPAnalytics.controllers', []);
    angular.module('TPAnalytics.directives', []);
}());