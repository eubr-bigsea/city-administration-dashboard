(function () {
    'use strict';

    angular.module("TPAnalytics")
        .factory('ranking_service', ["$rootScope", function($rootScope){
            $rootScope.selectedRoute = null;
            $rootScope.selectedDate = null;

            return {
                getRoute: function(){
                    return $rootScope.selectedRoute;
                },
                setRoute: function(route){
                    return $rootScope.selectedRoute = route;
                },
                getDate: function(){
                    return $rootScope.selectedDate;
                },
                setDate: function(date){
                    return $rootScope.selectedDate = date;
                }

            };
        }]);

}());


