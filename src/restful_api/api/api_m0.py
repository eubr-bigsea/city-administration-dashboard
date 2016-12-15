# -*- coding: utf-8 -*-

import datetime
import bd
import json
import util
from api import app
from flask import abort, request, make_response,Response
import funcoes_aux
from crossdomain import crossdomain

# Dado uma data e um onibus (4 digitos) retorna um json com todas as viagens daquela data
@app.route('/api/m0/get_travels/<data>/<bus>')
def api_get_travels(data,bus):
    return funcoes_aux.function_cors(funcoes_aux.montaJson(funcoes_aux.get_travels(data,bus)))

# Dado um onibus (4 digitos) retorna um json com todas as viagens de ontem
@app.route('/api/m0/get_travels_yesterday/<data>/<bus>')
def api_get_travels_yesterday(data, bus):
    data = datetime.date.fromordinal(datetime.datetime.strptime(data, "%Y-%m-%d").toordinal()-1).strftime("%Y-%m-%d")
    return api_get_route_trips(data,bus)

# Dado um onibus (4 digitos) retorna um json com todas as viagens anteriores a ontem
@app.route('/api/m0/get_travels_before_yesterday/<data>/<bus>')
def api_get_travels_before_yesterday(data, bus):
    data = datetime.datetime.now().strftime("%Y-%m-%d")
    return funcoes_aux.route_isEmpty(data,bus)

# Dado uma data e um onibus (4 digitos) retorna um json da tabela da sttp sabendo se é dia útil, sábado ou domingo
@app.route('/api/m0/frame_schedules/<data>/<bus>')
def api_get_frame_schedules(data,bus):
    return funcoes_aux.function_cors(funcoes_aux.montaJson(funcoes_aux.get_frame_schedules(data,bus)))

# Dado uma data e um onibus (4 digitos) retorna um json usado no gráfico do site de comparação(Dentro do horário, não cumpriu horário)
@app.route('/api/m0/route_trips/<data>/<bus>',methods=['GET','POST'])
def api_get_route_trips(data,bus):
    travels = funcoes_aux.get_travels_and_ticketing(data,bus)
    frame_schedules = funcoes_aux.get_frame_schedules(data,bus)

    return funcoes_aux.create_json_final(travels,frame_schedules,data,bus)

# Dado uma data e um onibus (4 digitos) retorna um json usado no gráfico do site de comparação(Dentro do horário, não cumpriu horário)
@app.route('/api/m0/route_trips_analysis/<start_data>/<end_data>',methods=['GET','POST'])
def api_get_route_trips_analysis(start_data,end_data):
    answer = "rota,data,hora_inicio,hora_fim,duracao,numero_onibus,hora_inicio_tb,hora_fim_tb,duracao_tb,del,operador,empresa,linha,pareado\n"
    start_date = datetime.datetime.strptime(start_data, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_data, '%Y-%m-%d')
    day_count = (end_date - start_date).days + 1

    route_list = funcoes_aux.get_all_routes()

    for route in route_list:
        route_aux = route["rota"].encode('utf-8')
        for single_date in (start_date + datetime.timedelta(n) for n in range(day_count)):
            data = datetime.datetime.strftime(single_date, '%Y-%m-%d') 
            travels = funcoes_aux.get_travels_analysis(data,route_aux)
            frame_schedules = funcoes_aux.get_frame_schedules(data,route_aux)
            for travel in funcoes_aux.create_json_final_analysis(travels,frame_schedules,data,route_aux):
                answer= answer+ travel
    return funcoes_aux.function_cors(answer)

# Dado uma data e um onibus (4 digitos) retorna um json usado no gráfico do site de comparação(Dentro do horário, não cumpriu horário)
@app.route('/api/m0/route_trips_and_ticketing_analysis/<start_data>/<end_data>',methods=['GET','POST'])
def api_get_route_trips_and_ticketing_analysis(start_data,end_data):
    start_date = datetime.datetime.strptime(start_data, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_data, '%Y-%m-%d')

    answer = funcoes_aux.get_route_trips_and_ticketing(start_date, end_date)

    return funcoes_aux.function_cors(answer)

# Dado uma data e um onibus (4 digitos) retorna um json usado no gráfico do site de comparação de todos os dados antes da data passada(Dentro do horário, não cumpriu horário)
#Dia tipico
@app.route('/api/m0/route_trips_before_days/<data>/<bus>',methods=['GET','POST'])
def api_get_route_trips_before_days(data,bus):
    travels = funcoes_aux.get_median_before_date(data,bus)
    frame_schedules = funcoes_aux.get_frame_schedules(data,bus)

    return funcoes_aux.create_json_final(travels,frame_schedules,data,bus)



# Dado uma data e um onibus (4 digitos) retorna um json usado no gráfico do site de comparação de três dias antes da data passada(Dentro do horário, não cumpriu horário)
@app.route('/api/m0/route_trips_between_tree_days/<data>/<bus>',methods=['GET','POST'])
def api_get_route_trips_between_tree_days(data,bus):
    travels = funcoes_aux.get_median_between_tree_days(data,bus)
    frame_schedules = funcoes_aux.get_frame_schedules(data,bus)

    return funcoes_aux.create_json_final(travels,frame_schedules,data,bus)



# Dado uma data e um onibus (4 digitos) retorna um json usado no gráfico do site de comparação de todos os dados da útilma semana(Dentro do horário, não cumpriu horário)
@app.route('/api/m0/route_trips_last_week/<data>/<bus>',methods=['GET','POST'])
def api_get_route_trips_last_week(data,bus):
    frame_schedules = funcoes_aux.get_frame_schedules(data,bus)
    travels = funcoes_aux.get_median_last_week(frame_schedules, data, bus)

    return funcoes_aux.median_of_travels(travels,data, bus)

# Dado uma data e um onibus (4 digitos) retorna um json usado no gráfico do site de comparação de todos os dados dos ultimos tres dias iguais(Dentro do horário, não cumpriu horário)
@app.route('/api/m0/route_trips_tree_equals_days/<data>/<bus>',methods=['GET','POST'])
def api_get_route_trips_tree_equals_days(data,bus):
    frame_schedule = funcoes_aux.get_frame_schedules(data,bus)
    travels = funcoes_aux.get_median_tree_equals_days(frame_schedule, data,bus)
    
    return funcoes_aux.median_of_travels(travels,data,bus)

# Retorna as rotas válidas
@app.route('/api/m0/valid_routes',methods=['GET','POST'])
def api_get_valid_routes():
    return funcoes_aux.function_cors(funcoes_aux.get_valid_routes())

@app.route('/api/m0/delay_ranking',methods=['GET','POST'])
def api_delay_ranking():
    return funcoes_aux.delay_ranking("")

@app.route('/api/m0/delay_ranking/<date>',methods=['GET','POST'])
def api_delay_ranking_date(date):
    return funcoes_aux.delay_ranking(str(date))

@app.route('/api/m0/route_trips_before_days_2/<data>/<bus>',methods=['GET','POST'])
def api_get_route_trips_before_days_2(data,bus):
    frame_schedules = funcoes_aux.get_frame_schedules(data,bus)
    travels = funcoes_aux.get_median_typical(frame_schedules, data, bus)

    return funcoes_aux.median_of_travels(travels,data, bus)

@app.route('/api/m0/route_trips_before_days_usual_days/<data>/<bus>',methods=['GET','POST'])
def api_get_route_trips_before_days_usual_days(data,bus):
    frame_schedules = funcoes_aux.get_frame_schedules(data,bus)
    travels = funcoes_aux.get_median_typical_usual_days(frame_schedules, data, bus)

    return funcoes_aux.median_of_travels(travels,data, bus)


# Api para grafico da tendencia da bilhetagem entre as empresas em determinado periodo de tempo
@app.route('/api/m0/time_stocking/<ticketing_type>/<start_date>/<end_date>',methods=['GET','POST'])
def time_stocking(ticketing_type,start_date,end_date):
    time_stocking_data = funcoes_aux.get_time_stocking_data(start_date, end_date)
    response = funcoes_aux.time_stocking(str(ticketing_type),time_stocking_data, start_date, end_date)
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

# Api para tendencia do atraso dos onibus com a bilhetagem
@app.route('/api/m0/del_durations_day/<year>',methods=['GET','POST'])
def del_durations_day(year):
    response = funcoes_aux.del_durations_day(int(year))
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

######## Autenticacao
@app.route('/api/m0/login/<usuario>/<senha>')
def login_admin(usuario, senha):
    response = "[{"+'"usuario"'+': '+ '"'+str(funcoes_aux.login(str(usuario), str(senha)))  +'"' +"}]"
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response
######################