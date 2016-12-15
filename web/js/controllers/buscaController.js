(function () {
    'use strict';

    angular.module("TPAnalytics.controllers")
        .controller("BuscaController", ["$scope",
            "dia_rota",
            "dia_tipico",
            "dia_tipico_especial",
            //"dia_anterior",
            //"ultimos_tres_dias",
            "ultima_semana",
            "ultimos_tres_dias_iguais",
            "rotas_validas",
            "dias_anteriores",
            "ranking_service",
            "$timeout",
            "$filter",
            function ($scope, dia_rota, dia_tipico,dia_tipico_especial, /*dia_anterior,*/ /*ultimos_tres_dias,*/ ultima_semana,
                      ultimos_tres_dias_iguais, rotas_validas, dias_anteriores, ranking_service, $timeout, $filter) {

                $scope.$on('$stateChangeStart', function(scope, next, current){
                    clearTips();
                });

                if (ranking_service.getRoute() == null){
                    $scope.rota = {selected: "020"};

                } else {
                    $scope.rota = {selected: ranking_service.getRoute()};
                    $scope.dt = ranking_service.getDate();

                }

                $scope.arc_chart_data = [];
                $scope.arc_chart_data2 = [];
                $scope.old_arc_chart_data = [];
                $scope.second_chart_getData_function = dia_tipico;
                $scope.seletoresIsEnable = true;
                $scope.dataIsLoaded = false;
                $scope.validDate = false;
                $scope.isDayType = true;
                $scope.valueRadio = { value:"all"};
                $scope.ticketingRadio = { value:"grouped"};
                $scope.currentChart = { value:"escala"};

                function clearTips(){
                    var tips = document.getElementsByClassName("d3-tip");
                    for (var i = 0; i < tips.length; i++){
                        tips[i].style.opacity = 0;
                    }
                }

                // Variáveis usadas para atualizar o cabeçalho no click de buscar
                $scope.rotaBarra = "";
                $scope.dataViagemBarra = "";

                $scope.routeMap = null;

                $scope.medianaDuracao = 0;
                rotas_validas.getData().success(function (data) {
                    $scope.routeMap = data.routes;
                    $scope.rotasValidas = Object.keys(data.routes).sort();
                    if(ranking_service.getRoute() == null) {
                        $scope.dt = new Date($scope.routeMap[$scope.rota.selected]);
                        $scope.dt.setDate($scope.dt.getDate() + 1);
                        $scope.maxDate = angular.copy($scope.dt);
                    }else {
                        $scope.maxDate = new Date($scope.routeMap[$scope.rota.selected]);
                        $scope.maxDate.setDate($scope.maxDate.getDate() + 1);
                    }
                    $scope.seletoresIsEnable = false;
                });

                // sai
                $scope.chart1WithoutTravels = false;
                $scope.chart1WithoutBus = false;
                //$scope.chart2WithoutTravels = false;

                $scope.update = function (form) {

                    if ($scope.checkDate()) {

                        dias_anteriores.getData($scope.rota.selected, $filter('date')($scope.dt, 'yyyy-MM-dd')).success(function (data) {
                            if (!data.isEmpty) {

                                dia_rota.getData($scope.rota.selected, $filter('date')($scope.dt, 'yyyy-MM-dd')).success(function (data) {
                                    $scope.rotaBarra = $scope.rota.selected;
                                    $scope.dataViagemBarra = $filter('date')($scope.dt, 'yyyy-MM-dd');
                                    $scope.arc_chart_data = data.nodes;
                                    $scope.old_arc_chart_data = $scope.arc_chart_data;
                                    $scope.chart1WithoutTravels = $scope.arc_chart_data.length === 0;
                                    $scope.lista_bus = data.list_bus;
                                    $scope.chart1WithoutBus = $scope.lista_bus.length === 0;
                                    $scope.listBusChecked = {};
                                    for (var i = 0; i < $scope.lista_bus.length; i++) {
                                        $scope.listBusChecked[$scope.lista_bus[i]] = true;
                                    }
                                    $scope.numViagensCorretas = (data.num_travels - (data.num_extra_travels + data.num_late_travels));
                                    $scope.numViagens = data.num_travels;
                                    $scope.numViagensMais = data.num_extra_travels;
                                    $scope.numViagensMenos = data.num_missing_travels;
                                    $scope.numViagensAtrasadas = data.num_late_travels;
                                    $scope.medianaDuracao = data.median;
                                    $scope.diaDaSemana = data.week_day;
                                    $scope.dataIsLoaded = true;
                                });

                                 $scope.second_chart_getData_function.getData($scope.rota.selected, $filter('date')($scope.dt, 'yyyy-MM-dd')).success(function (data) {
                                     $scope.arc_chart_data2 = data.nodes;
                                     $scope.chart2WithoutTravels = $scope.arc_chart_data2.length === 0;
                                     $scope.numViagens2 = $scope.arc_chart_data2.length;
                                     $scope.numViagensAtrasadas2 = data.num_late_travels;
                                     $scope.numViagensExtra2 = data.num_extra_travels;
                                     $scope.numViagensMenos2 = data.num_missing_travels;
                                     $scope.numViagensCorretas2 = $scope.numViagens2 - $scope.numViagensAtrasadas2 - $scope.numViagensMenos2
                                     $scope.medianaDuracao2 = data.median;
                                 });

                            } else {
                                $scope.chart1WithoutTravels = true;
                                //$scope.chart2WithoutTravels = true;
                                $timeout(function () {
                                    window.alert("Rota não possui viagens!");
                                });

                            }

                        });
                    }

                };

                $scope.$watch(function () {
                        return $scope.rota.selected;
                    },
                    function (newValue, oldValue) {

                        if ($scope.routeMap != null) {
                            $scope.dt = new Date($scope.routeMap[newValue]);
                            $scope.dt.setDate($scope.dt.getDate() + 1);

                            $scope.maxDate = new Date($scope.routeMap[newValue]);
                            $scope.maxDate.setDate($scope.maxDate.getDate() + 1);
                        }
                    }
                );

                $scope.updateTicketingRadio = function (value) {
                    $scope.ticketingRadio.value = value;
                };

                $scope.updateDiaTipico = function (value) {
                    if(value == undefined) {
                        $scope.valueRadio.value = "all";
                    }else {
                        $scope.valueRadio.value = value;
                    }
                    $scope.isDayType = true;
                    if ($scope.valueRadio.value == "all"){
                        $scope.second_chart_getData_function = dia_tipico;
                    }else{
                        $scope.second_chart_getData_function = dia_tipico_especial;
                    }

                    $scope.update();
                };

                $scope.updateTresUltimosDiasIguais = function () {
                    $scope.isDayType = false;
                    $scope.second_chart_getData_function = ultimos_tres_dias_iguais;

                    $scope.update();
                };

                $scope.updateUltimaSemana = function () {
                    $scope.isDayType = false;
                    $scope.second_chart_getData_function = ultima_semana;

                    $scope.update();
                };

                $scope.busClick = function(id) {
                    if (id == 'atrasadas') {
                        $scope.switches[0].isSelected = false;
                        $scope.switches[1].isSelected = true;
                        $scope.switches[2].isSelected = false;
                        $scope.switches[3].isSelected = false;

                    }else if (id == 'extra') {
                        $scope.switches[0].isSelected = false;
                        $scope.switches[1].isSelected = false;
                        $scope.switches[2].isSelected = true;
                        $scope.switches[3].isSelected = false;

                    } else if (id == 'faltantes') {
                        $scope.switches[0].isSelected = false;
                        $scope.switches[1].isSelected = false;
                        $scope.switches[2].isSelected = false;
                        $scope.switches[3].isSelected = true;

                    } else if (id == 'total') {
                        $scope.switches[0].isSelected = true;
                        $scope.switches[1].isSelected = true;
                        $scope.switches[2].isSelected = true;
                        $scope.switches[3].isSelected = false;

                    } else {
                        $scope.switches[0].isSelected = true;
                        $scope.switches[1].isSelected = false;
                        $scope.switches[2].isSelected = false;
                        $scope.switches[3].isSelected = false;
                    }
                };

                $scope.selectBus = function (bus) {
                    if ($scope.listBusChecked[bus]){
                        $scope.listBusChecked[bus] = false;
                    }
                    else{
                        $scope.listBusChecked[bus] = true;
                    }
                    $scope.check();
                };

                //mesma checkbox para os dois gráficos
                $scope.switches = [
                    {
                        id: "tolerado",
                        texto: "No horário tolerado",
                        isSelected: true
                    },
                    {
                        id: "atrasado",
                        texto: "Atrasadas",
                        isSelected: true
                    },
                    {
                        id: "extra",
                        texto: "Extra",
                        isSelected: false
                    },
                    {
                        id: "quadrohorario",
                        texto: "Faltantes",
                        isSelected: false
                    }
                ];

                $scope.colors = {
                    "tolerado": {"background": "#fee090", "border-color": "#fee090"},
                    "atrasado": {"background": "#d7191c", "border-color": "#d7191c"},
                    "extra": {"background": "#FC8918", "border-color": "#FC8918"},
                    "ideal": {"background": "#4575b4", "border-color": "#4575b4"},
                    "quadrohorario": {"background": "repeating-linear-gradient(-45deg,#4575b4,#4575b4 5px,#fff 5px,#fff 10px)", "border-color": "#4575b4"}
                };

                // ================== chart tips ========================== //

                $scope.tip = d3.tip()
                        .attr('class', 'd3-tip')
                        .offset([-10, 0])
                        .html(function(d) {
                            var answer = "Ônibus: " + d.numero_onibus +
                                "</br>Saída: " + $filter('date')(new Date("October 25, 1999 " + d.saida), 'HH:mm') +
                                "</br>Chegada: " + $filter('date')(new Date("October 25, 1999 " + d.chegada), 'HH:mm') +
                                "</br>Duração: " + d.duracao + " min" +
                                "</br>Diferença: " + d.del + " min";

                            if (d.ticketing !== undefined){
                                answer += "</br>Passageiros Inteiros: " + d.ticketing.inteiros +
                                          "</br>Passageiros Estudantes: " + d.ticketing.estudantes +
                                          "</br>Passageiros Gratuitos: " + d.ticketing.gratuitos +
                                          "</br>Equivalência: " + d.ticketing.equivalencia;
                            }
                            return answer;
                        });

                $scope.tipComparison = d3.tip()
                    .attr('class', 'd3-tip')
                    .offset([-10, 0])
                    .html(function(d) {
                        var answer = "Saída: " + $filter('date')(new Date("October 25, 1999 " + d.saida), 'HH:mm') +
                            "</br>Chegada: " + $filter('date')(new Date("October 25, 1999 " + d.chegada), 'HH:mm') +
                            "</br>Duração: " + d.duracao + " min" +
                            "</br>Diferença: " + d.del + " min";
                        if (d.num_faltou !== undefined){
                            answer += "</br>Faltou: " + d.num_faltou + " vezes";
                        }
                        return answer
                    });

                $scope.tipTicketing = d3.tip()
                    .attr('class', 'd3-tip')
                    .offset([-10, 0])
                    .html(function(d) {
                        var answer = "Pagantes: " + d.inteiros +
                        "</br>Estudantes: " + d.estudantes +
                        "</br>Gratuitos: " + d.gratuitos +
                        "</br>Total de passageiros: " + d.total +
                        "</br>Equivalencia: " + d.equivalencia;
                        return answer;
                    });

                // ================== end chart tips ====================== //

                $scope.check = function() {

                    $scope.resp = [];

                    for (var i = 0; i < $scope.old_arc_chart_data.length; i++){
                        if ($scope.old_arc_chart_data[i]["numero_onibus"] == "quadro_de_horario" || $scope.listBusChecked[$scope.old_arc_chart_data[i]["numero_onibus"]]){
                            $scope.resp.push($scope.old_arc_chart_data[i]);
                        }
                    }

                    var numViagensCertas = 0;
                    var numViagensAMais = 0;
                    var numViagensAMenos = 0;
                    var numViagensAtrasadas = 0;
                    var duracaoValores = [];
                    var median = 0;

                    for (var i = 0; i < $scope.resp.length; i++) {
                        if ($scope.resp[i]["numero_onibus"] == "quadro_de_horario"){
                            numViagensAMenos = numViagensAMenos + 1;
                        } else if($scope.resp[i]["pareado"] == false) {
                            numViagensAMais = numViagensAMais + 1;
                            duracaoValores.push($scope.resp[i]["duracao"]);
                        } else {
                            duracaoValores.push($scope.resp[i]["duracao"]);
                            if (Math.abs($scope.resp[i]["del"]) < 30){
                                numViagensCertas = numViagensCertas +1;
                            } else{
                                numViagensAtrasadas = numViagensAtrasadas+1;
                            }
                        }
                    }

                    duracaoValores = duracaoValores.sort();
                    var size = duracaoValores.length;
                    if (size == 0){
                        median = 0;
                    } else if (size % 2 == 0){
                        median = (duracaoValores[Math.floor(size/2)] + duracaoValores[Math.floor(size/2) - 1]) / 2.0;
                    }
                    else{
                        median = duracaoValores[Math.floor(size/2)];
                    }

                    $scope.numViagensCorretas = numViagensCertas;
                    $scope.numViagens = numViagensCertas+numViagensAMais+numViagensAtrasadas;
                    $scope.numViagensMais = numViagensAMais;
                    $scope.numViagensMenos = numViagensAMenos;
                    $scope.numViagensAtrasadas = numViagensAtrasadas;
                    $scope.medianaDuracao = median;

                    $scope.arc_chart_data = $scope.resp;
                };

                $scope.clean = function() {
                    for (var i = 0; i < $scope.lista_bus.length; i++) {
                        $scope.listBusChecked[$scope.lista_bus[i]] = false;
                    }
                    if($scope.lista_bus.length != 0) {
                        $scope.check()
                    }
                };


                // ========== CALENDAR ==========
                if($scope.dt == undefined) {
                    $scope.maxDate = new Date();
                    $scope.dt = $scope.maxDate;
                }

                $scope.open = function ($event) {
                    $scope.status.opened = true;
                };

                $scope.previousDay = function () {
                    $scope.dt = new Date($scope.dt.setDate($scope.dt.getDate() - 1));

                    $scope.update();
                };

                $scope.nextDay = function () {
                    var lastValidDate = $scope.maxDate;
                    if (!($scope.dt.getFullYear() == lastValidDate.getFullYear() && $scope.dt.getDate() == lastValidDate.getDate() && $scope.dt.getMonth() == lastValidDate.getMonth())) {
                        $scope.dt = new Date($scope.dt.setDate($scope.dt.getDate() + 1));
                        $scope.update();
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

                    if ($scope.dt !== undefined) {
                        var lastValidDate = $scope.maxDate;
                        var data = $scope.dt;

                        //tem que ser do último dia que tem dados ou antes
                        if (data > lastValidDate) {
                            erro = "A data deve ser no máximo " + $scope.maxDate.getDate() + "/" + ($scope.maxDate.getMonth() + 1) + "/" + $scope.maxDate.getFullYear();
                            check = false;
                        }
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
                $scope.update(null);

                $scope.comparisonChart = "typical_day";

                $scope.updateComparisonChart = function(chart, type){
                    $scope.comparisonChart = chart;
                    $scope.currentChart.value = type;

                    if (chart == "typical_day"){
                        $scope.updateDiaTipico();
                    } else if (chart == "last_three_equal_days"){
                        $scope.updateTresUltimosDiasIguais();
                    } else if (chart == "last_week"){
                        $scope.updateUltimaSemana();
                    }
                }

                $scope.slider_translate = {
                    minValue: 14400,
                    maxValue: 86400,
                    options: {
                        ceil: 86400,
                        floor: 14400,
                        translate: function (value) {
                            return $filter('date')(new Date(1970, 0, 1).setSeconds(value), 'HH:mm:ss')
                        }
                    }
                };
            }]);
}());

