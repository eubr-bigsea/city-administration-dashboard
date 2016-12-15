(function () {
    'use strict';

    angular.module("TPAnalytics.controllers")
        .controller("PanoramaController", ["$scope",
            "ranking_de_atrasos", "ranking_service", "$filter", "$timeout",
            function ($scope, ranking_de_atrasos, ranking_service, $filter, $timeout) {

                $scope.header = [
                    {name: "Rota", type: "route"},
                    {name: "Viagens Pontuais / Viagens Cumpridas", type: "punctual_travels"},
                    {name: "% Pontualidade", type: "punctuality_percentage"}
                ];

                $scope.headerMissing = [
                    {name: "Rota", type: "route"},
                    {name: "Viagens Cumpridas / Viagens Programadas", type: "total_of_paired_travels"},
                    {name: "% Cumpridas", type: "num_missing_travels_percentage"}
                ];

                $scope.headerExtra = [
                    {name: "Rota", type: "route"},
                    {name: "Viagens Extras / Viagens Feitas", type: "num_extra_travels"},
                    {name: "% Extra", type: "num_extra_travels_percentage"}
                ];

                $scope.sortReverse = true;
                $scope.sortParameter = "punctuality_percentage";
                $scope.delayRanking = null;

                $scope.missingTravelsRanking = null;
                $scope.sortReverseMissing = true;
                $scope.sortParameterMissing = "num_missing_travels_percentage";

                $scope.extraTravelsRanking = null;
                $scope.sortReverseExtra = true;
                $scope.sortParameterExtra = "num_extra_travels_percentage";

                $scope.setRoute = function(route){
                    ranking_service.setRoute(route);
                }

                $scope.setDate = function(date){
                    ranking_service.setDate(date);
                }

                $scope.rankingSort = function (sortParameter) {
                    $scope.sortParameter = sortParameter;
                    $scope.sortReverse = !$scope.sortReverse;
                }

                $scope.rankingSortMissing = function (sortParameterMissing) {
                    $scope.sortParameterMissing = sortParameterMissing;
                    $scope.sortReverseMissing = !$scope.sortReverseMissing;
                }

                $scope.rankingSortExtra = function (sortParameterExtra) {
                    $scope.sortParameterExtra = sortParameterExtra;
                    $scope.sortReverseExtra = !$scope.sortReverseExtra;
                }

                $scope.$watch(function () {
                        return $scope.delayRankingDate;
                    },
                    function (newValue, oldValue) {
                        if ($scope.delayRankingDate !== ranking_service.getDate() && $scope.checkDate()){
                            ranking_de_atrasos.getData($filter('date')(newValue, 'yyyy-MM-dd')).success(function (data) {
                                if ($scope.delayRankingDate == undefined) {

                                    $scope.delayRankingDate = new Date(data.date);
                                    $scope.delayRankingDate.setDate($scope.delayRankingDate.getDate() + 1);

                                    $scope.maxDate = new Date(data.date);
                                    $scope.maxDate.setDate($scope.maxDate.getDate() + 1);
                                }
                                $scope.setDate($scope.delayRankingDate);
                                $scope.delayRanking = data.delays;

                                $scope.missingTravelsRanking = data.delays;

                                $scope.extraTravelsRanking = data.delays;
                            });
                        }
                    }
                );

                // ========== CALENDAR ==========

                $scope.open = function ($event) {
                    $scope.status.opened = true;
                };

                $scope.previousDay = function () {
                    $scope.delayRankingDate = new Date($scope.delayRankingDate.setDate($scope.delayRankingDate.getDate() - 1));

                };

                $scope.nextDay = function () {
                    var lastValidDate = $scope.maxDate;
                    if (!($scope.delayRankingDate.getFullYear() == lastValidDate.getFullYear() && $scope.delayRankingDate.getDate() == lastValidDate.getDate() && $scope.delayRankingDate.getMonth() == lastValidDate.getMonth())) {
                        $scope.delayRankingDate = new Date($scope.delayRankingDate.setDate($scope.delayRankingDate.getDate() + 1));
                    }


                };

                $scope.dateOptions = {
                    formatYear: 'yy',
                    startingDay: 1
                };

                $scope.format = "dd/MM/yyyy";

                $scope.status = {
                    opened: false
                };

                $scope.checkDate = function () {
                    var check = true;
                    var erro = "Data inválida! Use o formato dd/MM/YYYY";

                    if ($scope.delayRankingDate !== undefined) {
                        var lastValidDate = $scope.maxDate;
                        var data = $scope.delayRankingDate;

                        //tem que ser do último dia que tem dados ou antes
                        if (data > lastValidDate) {
                            erro = "A data deve ser no máximo " + $scope.maxDate.getDate() + "/" + ($scope.maxDate.getMonth() + 1) + "/" + $scope.maxDate.getFullYear();
                            check = false;
                        }
                        $scope.validDate = false;
                    } else if ($scope.maxDate == undefined) {
                        check = true;
                        $scope.validDate = false;
                    } else {
                        check = false;
                    }

                    if (!check) {
                        $timeout(function () {
                            $scope.validDate = true;
                        });
                    }
                    return check;

                };

                // ======== END CALENDAR ========
            }]);
}());


