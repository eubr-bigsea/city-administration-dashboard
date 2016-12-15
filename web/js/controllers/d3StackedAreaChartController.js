(function () {
    'use strict';

    angular.module("TPAnalytics.controllers")
        .controller("StackedAreaChart", ["$scope", "equiv_overtime", function($scope, equiv_overtime){

            var opts = {
                chart: {
                    type: 'stackedAreaChart',
                    height: 450,
                    margin : {
                        top: 20,
                        right: 20,
                        bottom: 30,
                        left: 70
                    },
                    x: function(d){return d[0];},
                    y: function(d){return d[1];},
                    useVoronoi: false,
                    clipEdge: true,
                    duration: 100,
                    useInteractiveGuideline: true,
                    color: function(d, i){
                        switch(d.key){
                            case 'Nacional':
                                return '#0000FF';
                            case 'Transnacional':
                                return '#FF0000';
                            case 'Cabral':
                                return '#3366FF';
                            case 'SJ':
                                return '#333333';
                            case 'Cruzeiro':
                                return '#33CC00';
                            case 'Borborema':
                                return '#336600';
                        }
                    },
                    xAxis: {
                        showMaxMin: false,
                        tickFormat: function(d) {
                            return d3.time.format('%d/%m/%Y')(new Date(d*1000))
                        }
                    },
                    yAxis: {
                        tickFormat: function(d){
                            return d3.format(',.2f')(d);
                        }
                    },
                    interactiveLayer: {
                      tooltip: {
                          headerFormatter: function(d){
                              return d;
                          }
                      }
                    },
                    zoom: {
                        enabled: true,
                        scaleExtent: [1, 10],
                        useFixedDomain: false,
                        useNiceScale: false,
                        horizontalOff: false,
                        verticalOff: true,
                        unzoomEventType: 'dblclick.zoom'
                    }
                }
            };

            $scope.$watch(function () {
                    return $scope.data;
                },
                function (newValue, oldValue) {
                    if ($scope.data == undefined && $scope.options == undefined){
                        equiv_overtime.getData('equivalencia', '2015-06-28', '2015-10-28').success(function (data) {
                            $scope.data = data;
                            $scope.options = opts;
                        });
                    }
                }
            );

        }]);
}());
