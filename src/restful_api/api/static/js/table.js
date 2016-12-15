function primeiroDia(mesDoAno, ano, util) {
    var month = mesDoAno;
    var year = ano;

    var c = new Date();
    c.setFullYear(year, month, 1);

    var dayOfWeek = c.getDay();

    if (util) {
        while (dayOfWeek == 0 || dayOfWeek == 6) {
            c.setDate(c.getDate() + 1);
            dayOfWeek = c.getDay();
        }
    }

    return [c.getDate(), c.getDay()];
}

function primeiroDiaUtil(mesDoAno, ano) {
    return primeiroDia(mesDoAno, ano, true);
}

function isAnoBissexto(ano) {
    return new Date(ano, 1, 29).getMonth() == 1;
}

function numeroDeDias(mesDoAno, ano) {
    /* as datas do javascript funcionam pra fora do escopo do mês:
          o dia 0 de Maio é, na verdade, o último de Abril;
          o dia 32 de Janeiro, por sua vez, é 1o. de Fevereiro. */

    return (new Date(ano, mesDoAno + 1, 0).getDate());
}

function numeroDeSemanas(mesDoAno, ano) {
    /* geralmente, meses têm 5 semanas.
     um mês só pode ter 4 semanas se for Fevereiro, seu primeiro dia for Domingo e o ano não for bissexto
     um mês pode ter 6 semanas se:
            a) tiver 30 dias e seu primeiro dia for sábado; 
            b) tiver 31 dias e seu primeiro dia for sexta ou sábado. */

    var d = new Date(ano, mesDoAno, 1);
    var numeroDeDiasDoMes = numeroDeDias(mesDoAno, ano);
    var primeiroDiaDoMes = d.getDay();

    if ((numeroDeDiasDoMes == 30 && primeiroDiaDoMes == 5) || numeroDeDiasDoMes == 31 && primeiroDiaDoMes >= 5)
        return 6;
    if (d.getMonth() == 1 && new Date(ano, 1, 1).getDay() == 0 && !isAnoBissexto(ano))
        return 4;
    return 5;
}


function diasDoMes(mesDoAno, ano) {
    var semanas = [];
    var primeiraPosicao = primeiroDia(mesDoAno, ano, false);
    var diasComputados = 0;
    var numeroDeDiasDoMes = numeroDeDias(mesDoAno, ano);
    var numOfWeeks = numeroDeSemanas(mesDoAno, ano);

    for (var i = 1; i <= numOfWeeks; i++) {
        var dias = [];
        if (i == 1) {
            for (var j = 0; j < primeiraPosicao[1]; j++) {
                dias.push("");
            }

            for (var j = primeiraPosicao[1]; j < 7; j++) {
                diasComputados++;
                dias.push(diasComputados.toString());
            }
        } else if (i == numOfWeeks) {
            for (var j = 0; j < 7; j++) {
                diasComputados++;
                if (diasComputados > numeroDeDiasDoMes) {
                    dias.push("");
                } else {
                    dias.push(diasComputados.toString());
                }
            }

        } else {
            for (var j = 0; j < 7; j++) {
                diasComputados++;
                dias.push(diasComputados.toString());
            }
        }
        semanas.push(dias);
    }

    return semanas;
}

function CalendarioEscala(id, mesDoAno, ano, locaisDeFiscalizacao) {
    var divId = id;
    var daysOfWeek = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
    var daysOfMonth = diasDoMes(mesDoAno, ano);

    var drawn = false;
    var filled = false;

    var table = $("<table />");
    var tableHead = $("<thead />");
    var tableBody = $("<tbody />");

    var tableHeadRow = $("<tr />");

    var th = $("<th />");
    th.html("DIA");
    tableHeadRow.append(th);

    for (var i = 0; i < daysOfWeek.length; i++) {
        th = $("<th />");
        th.html(daysOfWeek[i]);
        tableHeadRow.append(th);
    }

    table.addClass("table table-bordered table-striped table-hover table-condensed celula");

    tableHead.append(tableHeadRow);
    table.append(tableHead);
    table.append(tableBody);
    this.draw = function () {
        if (drawn) {
            return;
        }

        $("#" + divId).append(table);
        drawn = true;
    };

    this.adicionarLinhaDeDias = function() {
        var weekVals = daysOfMonth.shift();

        var tr = $("<tr />");
        var td = $("<td />");
        td.html("Data");

        tr.append(td);

        for (var i = 0; i < daysOfWeek.length; i++) {
            td = $("<td />");
            td.html(weekVals.shift());
            tr.append(td);
        }

        tableBody.append(tr);
    };

    this.preencher = function(locaisDeFiscalizacao) {
        if (filled) {
            return;
        }

        for (var i = 0; i < numeroDeSemanas(mesDoAno, ano); i++) {
            this.adicionarLinhaDeDias();
            for (var j = 0; j < locaisDeFiscalizacao.length; j++) {
                this.adicionarLocalDeFiscalizacao(locaisDeFiscalizacao[j]);
            }
        }

        filled = true;
    };

    this.adicionarLocalDeFiscalizacao = function (local) {
        var tr = $("<tr />");
        var td = $("<td />");
        td.html("<strong>" + local[1] + "</strong>");

        tr.append(td);

        for (var i = 0; i < daysOfWeek.length; i++) {
            td = $("<td />");
            tr.append(td);
        }

        tableBody.append(tr);
    };
}
