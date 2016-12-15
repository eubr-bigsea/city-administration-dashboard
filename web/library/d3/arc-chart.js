function arc_chart(scope, element, attrs) {

   // graph = data;

    var yValue = 300;
    var width  = $(window).width();         // width of svg image
    var height =  $(window).height();        // height of svg image
    var margin = 10;            		// amount of margin around plot area
    var pad = (margin) / 2;       		// actual padding amount
    var radius = 4;             		// fixed node radius
    var yfixed = pad + radius;  		// y position for all nodes

    var chart =  d3.select("#chart");
    var aspX = 960;
    var aspY = 500;
    var aspect = aspX / aspY;
    var dOk = 10;
    var dTol = 20;
    var dErr = 30;

// Generates a tooltip for a SVG circle element based on its ID
    function addTooltip(circle) {
        var x = parseFloat(circle.attr("cx"));
        var y = parseFloat(circle.attr("cy"));
        var r = parseFloat(circle.attr("r"));
        var text = circle.attr("id");

        var tooltip = d3.select("#plot")
            .append("text")
            .text(text)
            .attr("x", x)
            .attr("y", y)
            .attr("dy", -r * 2)
            .attr("id", "tooltip");

        var offset = tooltip.node().getBBox().width / 2;

        if ((x - offset) < 0) {
            tooltip.attr("text-anchor", "start");
            tooltip.attr("dx", -r);
        }
        else if ((x + offset) > (width - margin)) {
            tooltip.attr("text-anchor", "end");
            tooltip.attr("dx", r);
        }
        else {
            tooltip.attr("text-anchor", "middle");
            tooltip.attr("dx", 0);
        }
    }


    function updateArcDraw(graph){

        chart.selectAll("path").remove();
        chart.selectAll("g").remove();
        chart.selectAll("line").remove();

        var panelB = $("div#panel-body1");
        chart = d3.select(".container").select("svg")
            .attr("id", "plot")
            .attr("width", panelB.width())
            .attr("height", panelB.width() / aspect)
        ;
        arcDraw(graph.nodes);
        yLinesDraw();

        console.log(panelB.width());
        console.log(panelB.height());
    }



    function draw(graph){

        // Função para atualizar gráfico quando ocorre resize
        $(window).resize(function() {
            updateArcDraw(graph);
        });
        // console.log($('input[id="atrasado"]')[0].checked);
        $(".checkbox").on("change", function(d, i){
            updateArcDraw(graph);
        });

        updateArcDraw(graph);

    }



    function arcDraw(data) {

        var pi = Math.PI;
        var arc = d3.svg.arc()
            .innerRadius((function(d, i){return ((d.duracao/2.5) - 3);}))
            .outerRadius(function(d, i){return ((d.duracao/2.5));})
            .startAngle(2.5 *pi)
            .endAngle(1.5 *pi);

        chart.selectAll("path")
            .attr("class", "data")
            .data(data)
            .enter().append("svg:path")
            .style("opacity",  function(d, i){
                if(d.del >= 30){
                    return 0.90;

                } else if (d.del < 30) {
                    return 0.7;
                }})
            .style("fill", function(d, i){

                //tentando implementar a mudança na cor assim q desmarcar...
                if (Math.abs(d.del) >= dTol & Math.abs(d.del) < dErr & $('input[id="tolerado"]')[0].checked == true){
                    return "chocolate";
                } else if (Math.abs(d.del) >= dTol & Math.abs(d.del) < dErr & $('input[id="tolerado"]')[0].checked == false) {
                    return "transparent";
                }
                else if(Math.abs(d.del) >= dErr & $('input[id="atrasado"]')[0].checked == true)
                    return "red";
                else if(Math.abs(d.del) >= dErr & $('input[id="atrasado"]')[0].checked == false)
                    return "transparent";
                else if($('input[id="normal"]')[0].checked == true)
                    return "khaki";
                else if($('input[id="normal"]')[0].checked == false)
                    return "transparent";
            }).attr("d", arc).attr("transform",function(d, i){
                return "translate("+((d.saida_ajuste/1.28)+(d.duracao/2.5))+","+yValue+")";})
            .attr("id", function(d, i) { return "Ônibus: "+d.numero_onibus+". Saida: "+d.saida+". Chegada: "+d.chegada+". Saida: "+d.saida_ajuste+"."+". Duracao: "+d.duracao+"."; })
            .attr("cx", function(d, i) { return 4; })
            .attr("cy", function(d, i) { return 22; })
            .attr("r",  function(d, i) { return radius; })
            .on("mouseover", function(d, i) {

                if (Math.abs(d.del) >= dTol & Math.abs(d.del) < dErr & $('input[id="tolerado"]')[0].checked == true)
                    addTooltip(d3.select(this));
                else

                if((Math.abs(d.del) >= dErr) & $('input[id="atrasado"]')[0].checked == true)
                    addTooltip(d3.select(this));
                else
                if((Math.abs(d.del) < dTol) & $('input[id="normal"]')[0].checked == true)
                    addTooltip(d3.select(this));

            })
            .on("mouseout", function(d, i) {

                if (Math.abs(d.del) >= dTol & Math.abs(d.del) < dErr & $('input[id="tolerado"]')[0].checked == true)
                    d3.select("#tooltip").remove();


                if(Math.abs(d.del) >= dErr & $('input[id="atrasado"]')[0].checked == true)
                    d3.select("#tooltip").remove();

                if(Math.abs(d.del) < dTol & $('input[id="normal"]')[0].checked == true)
                    d3.select("#tooltip").remove();

            });
    }



// ok
    function yLinesDraw(){

        xZ = d3.scale.ordinal()
            .domain([4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
            .rangePoints([1, aspX-20]);

        xAxis = d3.svg.axis()
            .scale(xZ)
            .orient("bottom");

        chart.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate("+ 1 +"," + yValue + ")")
            .call(xAxis);

        chart.append("line")          // attach a line
            .style("stroke", "grey")
            .style("stroke-dasharray", ("5, 5"))  // colour the line
            // adicionando linhas verticais
            .attr("x1", 2)     // x position of the first end of the line
            .attr("y1", 10)      // y position of the first end of the line
            .attr("x2", 2)     // x position of the second end of the line
            .attr("y2", yValue);    // y position of the second end of the line


    }

}