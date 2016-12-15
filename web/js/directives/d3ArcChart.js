(function () {
    'use strict';

    angular.module('TPAnalytics.directives')
        .directive('d3Bars', ["$filter", function($filter) {
            return {
                restrict: 'EA',
                scope: {
                    data: "=",
                    switches: "=",
                    median: "=",
                    colors: "=",
                    tip: "=",
                    comparison: "=",
                    slider: "=",
                    label: "@",
                    onClick: "&"
                },
                link: function(scope, iElement, iAttrs) {
                    var aspX = 960;
                    var aspY = 500;
                    var aspect = aspX / aspY;
                    var margin = 120;            		// amount of margin around plot area
                    var pad = (margin) / 2;       		// actual padding amount
                    var thisBefore = null;
                    var clicked = null;
                    var dBefore = null;

                    var w = angular.element(window);
                    scope.getWindowDimensions = function () {
                        return {
                            'h': w[0].innerHeight,
                            'w': w[0].innerWidth
                        };
                    };

                    var svgWidth = scope.getWindowDimensions().w;
                    var svgHeight = scope.getWindowDimensions().h / 3;
                    var arcProportion = (svgWidth / 940);

                    var svg = d3.select(iElement[0])
                        .append("svg")
                        .attr("width", svgWidth - pad)
                        .attr("height", svgHeight - pad);

                    svg.call(scope.tip);

                    scope.$watch(scope.getWindowDimensions, function (newValue, oldValue) {
                        svg = svg.attr("width", svgWidth - margin);
                    }, true);

                    w.bind('resize', function () {
                        scope.$apply();
                    });

                    scope.$watch('comparison', function(newVals, oldVals) {
                        if (dBefore != null && thisBefore != null && scope.comparison != null){
                            removeHighlight(dBefore, thisBefore);
                            dBefore = null;
                            thisBefore = null;
                            clicked = null;
                        }
                    }, true);

                    // watch for data changes and re-render
                    scope.$watch('data', function(newVals, oldVals) {
                        return scope.render(newVals, scope.switches, scope.median, scope.slider);
                    }, true);

                    scope.$watch('switches', function(newVals, oldVals) {
                        return scope.render(scope.data, newVals, scope.median, scope.slider);
                    }, true);

                    scope.$watch('median', function(newVals, oldVals) {
                        return scope.render(scope.data, scope.switches, newVals, scope.slider);
                    }, true);

                    scope.$watch('slider', function(newVals, oldVals) {
                        return scope.render(scope.data, scope.switches, scope.median, newVals);
                    }, true);

                    // define render function
                    function removeHighlight(d, that) {
                        scope.tip.hide(d);
                        d3.select(that).attr("stroke", 'none');
                        svg.selectAll("path").style("opacity", "0.9");
                        svg.selectAll("#viagem_ideal").remove();
                    }

                    function timeToFloat(time) {
                        var time = time.split(":");
                        return parseFloat(time[0]) + parseFloat(time[1]) / 60 + parseFloat(time[2]) / 3600;
                    }

                    function draw_ideal_arc(pi, d, radius, that, xZ) {
                        var arc = d3.svg.arc()
                            .innerRadius((function (d, i) {
                                return ((d.duracao_tb / 2.5) - 3) * arcProportion;
                            }))
                            .outerRadius(function (d, i) {
                                return ((d.duracao_tb / 2.5)) * arcProportion;
                            })
                            .startAngle(2.5 * pi)
                            .endAngle(1.5 * pi);

                        svg.selectAll("path").select("g")
                            .attr("class", "data")
                            .data([d])
                            .enter().append("svg:path")
                            .style("opacity", "0.9")
                            .style("fill", scope.colors["ideal"]["background"]) //MUDA A COR AQUI
                            .attr("d", arc).attr("transform", function (d, i) {
                                return "translate(" + (xZ(timeToFloat(d.saida_tb)) + (d.duracao_tb / 2.5) * arcProportion) + "," + (svgHeight - 85) + ")";
                            }) //yValue substituido por 130
                            .attr("id", function (d, i) {
                                return "viagem_ideal";
                            })
                            .attr("cx", function (d, i) {
                                return 4;
                            })
                            .attr("cy", function (d, i) {
                                return 22;
                            })
                            .attr("r", function (d, i) {
                                return radius;
                            })

                        that.parentNode.appendChild(that);
                    }

                    function change_arc_opacity() {
                        svg.selectAll("path").style("opacity", '0.3');
                        d3.select(this).attr("stroke", 'rgba(0, 0, 0, 0.8)');
                        d3.select(this).style("opacity", '0.9');
                        d3.select(".domain").style("opacity", '1');
                    }

                    function hourToSec(hour) {
                        var timeArray = hour.split(":").map(Number);
                        return timeArray[0] * 3600 + timeArray[1] * 60 + timeArray[2];
                    }

                    scope.render = function(data, switches, median, slider){
                        // remove all previous items before render
                        svg.selectAll("*").remove();
                        if (dBefore !== null && thisBefore !== null) {
                            removeHighlight(dBefore, thisBefore);
                            clicked = null;
                            dBefore = null;
                            thisBefore = null;
                        }

                        var yValue = 300;
                        var width = $(window).width;        // width of svg image
                        var height = $(window).height();    // height of svg image
                        var radius = 4;             		// fixed node radius
                        var yfixed = pad + radius;  		// y position for all nodes

                        var dTol = 20;
                        var dOk = 10;
                        var dErr = 30;

                        var xZ = d3.scale.linear()
                            .domain([4, 24])
                            .range([1, svgWidth - margin - 20]);

                        var xAxis = d3.svg.axis()
                            .scale(xZ)
                            .orient("bottom")
                            .ticks(21);

                        svg.append("g")
                            .attr("class", "x axis")
                            .attr("transform", "translate(" + 1 + "," + (svgHeight - 85) + ")")
                            .call(xAxis);

                        svg.append('pattern')
                            .attr('id', 'diagonalHatch')
                            .attr('patternUnits', 'userSpaceOnUse')
                            .attr('width', 4)
                            .attr('height', 4)
                            .append('path')
                            .attr('d', 'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2')
                            .attr('stroke', scope.colors["quadrohorario"]["border-color"])
                            .attr('stroke-width', 1);

                        var enableUnclick = true;
                        var pi = Math.PI;
                        var arc = d3.svg.arc()
                            .innerRadius((function (d, i) {
                                return ((d.duracao / 2.5) - 3) * arcProportion;
                            }))
                            .outerRadius(function (d, i) {
                                return (d.duracao / 2.5) * arcProportion;
                            })
                            .startAngle(2.5 * pi)
                            .endAngle(1.5 * pi);

                        var highlight = function (d, that) {
                            var saidaSec = hourToSec(d.saida);
                            var chegadaSec = hourToSec(d.chegada);

                            if(saidaSec >= slider.minValue && chegadaSec <= slider.maxValue) {
                                if (d.tipo_viagem == "extra" && switches[2].isSelected) {
                                    scope.tip.show(d);
                                    d3.select(that).attr("stroke", 'rgba(0, 0, 0, 0.8)');
                                } else if ( (d.tipo_viagem == "tolerado" && switches[0].isSelected) ||
                                    (d.tipo_viagem == "atrasado" && switches[1].isSelected))  {
                                    scope.tip.show(d);
                                    change_arc_opacity.call(that);
                                    draw_ideal_arc(pi, d, radius, that, xZ);
                                } else if (d.tipo_viagem == "faltante" && switches[3].isSelected) {
                                    scope.tip.show(d);
                                    d3.select(that).attr("stroke", 'rgba(0, 0, 0, 0.8)');
                                }
                            }
                        };

                        svg.on("click", function(){
                            if (enableUnclick){
                                if(dBefore != null && thisBefore != null){
                                    removeHighlight(dBefore, thisBefore);
                                    clicked = null;
                                    dBefore = null;
                                    thisBefore = null;
                                }
                            } else {
                                enableUnclick = true;
                            }
                        })


                        svg.selectAll("path").select("g")
                            .attr("class", "data")
                            .data(data)
                            .enter().append("svg:path")
                            .style("opacity", "0.9")
                            .style("fill", function (d, i) {
                                var saidaSec = hourToSec(d.saida);
                                var chegadaSec = hourToSec(d.chegada);

                                if(saidaSec >= slider.minValue && chegadaSec <= slider.maxValue) {
                                    if (d.tipo_viagem == "tolerado") {
                                        if (switches[0].isSelected == true) {
                                            return scope.colors["tolerado"]["background"]; // orangered chocolate
                                        } else {
                                            return "transparent";
                                        }
                                    } else if (d.tipo_viagem == "atrasado") {
                                        if (switches[1].isSelected == true) {
                                            return scope.colors["atrasado"]["background"]; // darkred red firebrick
                                        } else {
                                            return "transparent";
                                        }
                                    } else if (d.tipo_viagem == "extra") {
                                        if (switches[2].isSelected == true) {
                                            return scope.colors["extra"]["background"];
                                        } else {
                                            return "transparent";
                                        }
                                    } else if (d.tipo_viagem == "faltante") {
                                        if (switches[3].isSelected == true) {
                                            return "url(#diagonalHatch)";
                                        } else {
                                            return "transparent";
                                        }
                                    }
                                }else {
                                    return "transparent"
                                }
                            })
                            .attr("d", arc).attr("transform", function (d, i) {
                                return "translate(" + (xZ(timeToFloat(d.saida)) + (d.duracao / 2.5) * arcProportion) + "," + (svgHeight - 85) + ")";
                            }) //yValue substituido por 130
                            .attr("id", function (d, i) {
                                return "Ônibus: " + d.numero_onibus + ". Saída: " + d.saida + ". Chegada: " + d.chegada + ". Duração: " + d.duracao + ".";
                            })
                            .attr("cx", function (d, i) {
                                return 4;
                            })
                            .attr("cy", function (d, i) {
                                return 22;
                            })
                            .attr("r", function (d, i) {
                                return radius;
                            })
                            .on('mouseout', function (d) {
                                if (clicked == null) {
                                    removeHighlight(d, this);
                                }
                            })
                            .on('mouseover', function (d) {
                                if(clicked == null) {
                                    highlight(d, this);
                                }
                            })
                            .on('click', function (d) {
                                enableUnclick = false;
                                if (dBefore != null || thisBefore != null){
                                    removeHighlight(dBefore, thisBefore);
                                }

                                if (clicked == d.chegada + d.chegada_tb + d.saida + d.saida_tb) {
                                    clicked = null;
                                    dBefore = null;
                                    thisBefore = null;

                                } else {
                                    thisBefore = this;
                                    dBefore = d;
                                    clicked = d.chegada + d.chegada_tb + d.saida + d.saida_tb;

                                    highlight(d, this);
                                }
                            });

                    };
                }
            };
        }]);
}());