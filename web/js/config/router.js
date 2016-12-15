(function () {
    'use strict';

    angular.module("TPAnalytics")
        .config(function($stateProvider, $urlRouterProvider) {

            $urlRouterProvider.otherwise('/index/login');

            $stateProvider
                .state('index', {
                    url: '/index',
                    templateUrl: 'index.html',
                    data: {
                        requireLogin: false
                    }
                })
                .state('index.conteudo', {
                    url: '/conteudo',
                    controller: 'MainController',
                    templateUrl: 'conteudo.html',
                    data: {
                        requireLogin: false
                    }
                })
                .state('index.login', {
                    url: '/login',
                    controller: 'LoginController',
                    templateUrl: 'login.html',
                    data: {
                        requireLogin: false
                    }
                })
                .state('index.conteudo.panorama', {
                    url: '/panorama',
                    controller: 'PanoramaController',
                    templateUrl: 'panorama.html',
                    data: {
                        requireLogin: true
                    }
                })
                .state('index.conteudo.graficosHorarios', {
                    url: '/graficosHorarios',
                    controller: 'BuscaController',
                    templateUrl: 'schedule_chart.html',
                    data: {
                        requireLogin: true
                    }
                })
                .state('index.conteudo.analises', {
                    url: '/analises',
                    //controller: 'BuscaController',
                    templateUrl: 'analises.html',
                    data: {
                        requireLogin: true
                    }
                })
                .state('index.conteudo.tendencias', {
                    url: '/tendencias',
                    //controller: 'd3StackedAreaChartController',
                    templateUrl: 'tendencias.html',
                    data: {
                        requireLogin: true
                    }
                });

        }).run(function ($rootScope) {

            $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
                var requireLogin = toState.data.requireLogin;

                if (requireLogin && typeof $rootScope.currentUser === 'undefined') {
                    event.preventDefault();
                    window.location.replace('#/index/login');
                }

                //if (typeof angular == 'undefined'){
                //    window.location.replace('/index/login');
                //}
            });

    });

}());
