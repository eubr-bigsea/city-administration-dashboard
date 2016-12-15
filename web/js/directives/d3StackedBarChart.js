(function () {
    'use strict';

    angular.module('TPAnalytics.directives')
        .directive('d3StackedBar', [function() {
            return {
                restrict: 'EA',
                scope: {
                    data: "=",
                    radio: "=",
                    tip: "=",
                    switches: "=",
                    comparison: "=",
                    slider: "=",
                    label: "@",
                    onClick: "&"
                },
                link: function(scope, iElement, iAttrs) {

                var aspX = 960;
                var aspY = 320;
                var aspect = aspX / aspY;
                var margin = 120;            		// amount of margin around plot area
                var pad = (margin) / 2;       		// actual padding amount
                var dBefore = null;

                var parentElement = iElement[0].parentElement.parentElement.parentElement.parentElement;

                var w = angular.element(window);
                scope.getWindowDimensions = function () {
                    return {
                        'h': w[0].innerHeight,
                        'w': w[0].innerWidth
                    };
                };

                var svgWidth = scope.getWindowDimensions().w;
                var svgHeight = scope.getWindowDimensions().h / 3;

                var margin2 = {top: 40, right: 10, bottom: 20, left: 10},
                    width = 1700 - margin2.left - margin2.right,
                    height = 320 - margin2.top - margin2.bottom;

                var svg = d3.select(iElement[0]).append("svg")
                    .attr("width", svgWidth - pad)
                    .attr("height", svgHeight - pad)
                    .append("g")
                    //.attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");


                svg.call(scope.tip);

                scope.$watch('comparison', function(newVals, oldVals) {
                    if (dBefore != null){
                        removeHighlight(dBefore);
                        dBefore = null;
                    }
                }, true);

                scope.$watch('radio', function(newVals, oldVals) {
                    if (scope.data.length != 0){
                        return scope.render(scope.data, newVals, scope.slider);
                    }
                }, true);

                // watch for data changes and re-render
                scope.$watch('data', function(newVals, oldVals) {
                    if (scope.data.length != 0){
                        return scope.render(newVals, scope.radio, scope.slider);
                    }
                }, true);

                // watch for data changes and re-render
                scope.$watch('switches', function(newVals, oldVals) {
                    if (scope.data.length != 0){
                        return scope.render(scope.data, scope.radio, scope.slider);
                    }
                }, true);

                scope.$watch('slider', function(newVals, oldVals) {
                    if (scope.data.length != 0){
                        return scope.render(scope.data, scope.radio, scope.slider);
                    }
                }, true);

                function hourToSec(hour) {
                    var timeArray = hour.split(":").map(Number);
                    return timeArray[0] * 3600 + timeArray[1] * 60 + timeArray[2];
                }

                function getDictHours(travels, slider){
                    var dict_hours = {};

                    for (var i = 0; i<travels.length;i++){

                        var saidaSec = hourToSec(travels[i]["saida"]);
                        var chegadaSec = hourToSec(travels[i]["chegada"]);

                        if(saidaSec >= slider.minValue && chegadaSec <= slider.maxValue) {
                            var hour = parseInt(travels[i]["saida"].split(":")[0]);
                            if (travels[i]["tipo_viagem"] != "faltante" &&
                                ((travels[i]["tipo_viagem"] == "tolerado" && scope.switches[0].isSelected) ||
                                    (travels[i]["tipo_viagem"] == "atrasado" && scope.switches[1].isSelected) ||
                                    (travels[i]["tipo_viagem"] == "extra" && scope.switches[2].isSelected)
                                )) {
                                if (!(hour in dict_hours)) {
                                    dict_hours[hour] = {"gratuitos": travels[i]["ticketing"]["gratuitos"],
                                        "estudantes":travels[i]["ticketing"]["estudantes"],
                                        "inteiros": travels[i]["ticketing"]["inteiros"],
                                        "equivalencia": parseFloat(travels[i]["ticketing"]["equivalencia"])};
                                }
                                else{
                                    dict_hours[hour]["gratuitos"] = dict_hours[hour]["gratuitos"]+ travels[i]["ticketing"]["gratuitos"];
                                    dict_hours[hour]["estudantes"] = dict_hours[hour]["estudantes"] + travels[i]["ticketing"]["estudantes"];
                                    dict_hours[hour]["inteiros"] = dict_hours[hour]["inteiros"] + travels[i]["ticketing"]["inteiros"];
                                    dict_hours[hour]["equivalencia"] = parseFloat(dict_hours[hour]["equivalencia"])+parseFloat(travels[i]["ticketing"]["equivalencia"]);
                                }
                            }
                        }
                    }
                    return dict_hours
                }

                function highlight(d){
                    scope.tip.show(d);
                }

                function removeHighlight(d){
                    scope.tip.hide(d);
                }

                function getTicketing(travels, slider) {

                    var dict_hours = getDictHours(travels, slider);

                    var result_list = [[],[],[]];

                    var list_keys = Object.keys(dict_hours);
                    list_keys.sort();
                    var inteiros, estudantes, gratuitos, total, equivalencia;
                    for (var i = 0; i<list_keys.length;i++){
                        if (list_keys[i] >=4){
                            inteiros = parseInt(dict_hours[parseInt(list_keys[i])]["inteiros"]);
                            estudantes = parseInt(dict_hours[parseInt(list_keys[i])]["estudantes"]);
                            gratuitos = parseInt(dict_hours[parseInt(list_keys[i])]["gratuitos"]);
                            total = inteiros + estudantes + gratuitos;
                            equivalencia = parseFloat(dict_hours[parseInt(list_keys[i])]["equivalencia"]);

                            result_list[0].push({ "x":list_keys[i], "y":inteiros, "inteiros": inteiros, "estudantes": estudantes, "gratuitos": gratuitos, "total": total, "equivalencia": equivalencia});
                            result_list[1].push({ "x":list_keys[i], "y":estudantes, "inteiros": inteiros, "estudantes": estudantes, "gratuitos": gratuitos, "total": total, "equivalencia": equivalencia});
                            result_list[2].push({ "x":list_keys[i], "y":gratuitos, "inteiros": inteiros, "estudantes": estudantes, "gratuitos": gratuitos, "total": total, "equivalencia": equivalencia});
                        }
                    }

                return result_list;
                }

                scope.render = function(data, radio, slider){
                    if (dBefore != null){
                        removeHighlight(dBefore);
                        dBefore = null;
                    }

                    data = getTicketing(data, slider);

                    svg.selectAll("*").remove();

                    var n = 3, // number of layers
                        m = 25, // number of samples per layer
                        index = -1,
                        stack = d3.layout.stack(),
                        layers = stack(d3.range(n).map(function() { index += 1; return data[index]; })),
                        yGroupMax = d3.max(layers, function(layer) { return d3.max(layer, function(d) { return d.y; }); }),
                        yStackMax = d3.max(layers, function(layer) { return d3.max(layer, function(d) { return d.y0 + d.y; }); });

                    var x = d3.scale.ordinal()
                        .domain(d3.range(4,m))
                        .rangeRoundBands([0, svgWidth - margin - 20], .08);

                    var y = d3.scale.linear()
                        .domain([0, yStackMax])
                        .range([svgHeight - pad - 20, 0]);

                    var color = d3.scale.linear()
                        .domain([0, n - 1])
                        .range(["#4575b4", "#556"]);

                    var xAxis = d3.svg.axis()
                        .scale(x)
                        .tickSize(0)
                        .tickPadding(6)
                        .orient("bottom");

                    var layer = svg.selectAll(".layer")
                        .data(layers)
                      .enter().append("g")
                        .attr("class", "layer")
                        .style("fill", function(d, i) { return color(i); });

                    var rect = layer.selectAll("rect")
                        .data(function(d) { return d; })
                      .enter().append("rect")
                        .attr("x", function(d) { return x(d.x); })
                        .attr("y", svgHeight - pad - 20)
                        .attr("width", x.rangeBand())
                        .attr("height", 0);

                    rect.transition()
                        .delay(function(d, i) { return i * 10; })
                        .attr("y", function(d) { return y(d.y0 + d.y); })
                        .attr("height", function(d) { return y(d.y0) - y(d.y0 + d.y); });

                    svg.append("g")
                        .attr("class", "x axis")
                        .attr("transform", "translate(0," + (svgHeight - pad - 20) + ")")
                        .call(xAxis);

                    layer.selectAll("rect")
                        .data(function(d) { return d; })
                        .on('mouseout', function (d) {
                            if (dBefore == null){
                                removeHighlight(d);
                            }
                        })
                        .on('mouseover', function (d) {
                            if (dBefore == null){
                                highlight(d);
                            }
                        }).on('click', function(d){
                            if (dBefore != null){
                                removeHighlight(dBefore);
                            }

                            if (d == dBefore) {
                                dBefore = null;
                            } else {
                                highlight(d);
                                dBefore = d;
                            }
                        });

                    function transitionGrouped() {
                      y.domain([0, yGroupMax]);

                      rect.transition()
                          .duration(500)
                          .delay(function(d, i) { return i * 10; })
                          .attr("x", function(d, i, j) { return x(d.x) + x.rangeBand() / n * j; })
                          .attr("width", x.rangeBand() / n)
                        .transition()
                          .attr("y", function(d) { return y(d.y); })
                          .attr("height", function(d) { return svgHeight -pad - 20 - y(d.y); });
                    }

                    function transitionStacked() {
                      y.domain([0, yStackMax]);

                      rect.transition()
                          .duration(500)
                          .delay(function(d, i) { return i * 10; })
                          .attr("y", function(d) { return y(d.y0 + d.y); })
                          .attr("height", function(d) { return y(d.y0) - y(d.y0 + d.y); })
                        .transition()
                          .attr("x", function(d) { return x(d.x); })
                          .attr("width", x.rangeBand());
                    }


                    clearTimeout(2);
                    if (radio.value === "grouped") {
                        transitionGrouped();
                    } else {
                        transitionStacked();
                    }

                }
            }
        };
    }]);
}());