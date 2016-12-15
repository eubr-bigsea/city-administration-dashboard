(function () {
    'use strict';

    angular.module("TPAnalytics.controllers")
        .controller("LoginController", ["$scope", "loginService",
            function ($scope, loginService) {
                $scope.login = null;
                $scope.password = null;
                
                $scope.submit = function(){
                    loginService.checkAuth($scope.login, $scope.password);
                };
            }]);
}());



