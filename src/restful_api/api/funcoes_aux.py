## Essa linha de codigo abaixo(comentario) foi colocada para dizer a codificacao do python, se retirar ele quebra
# -*- coding: utf-8 -*-
import json
import collections
import operator
import datetime
import time
import bd
from api import app
from flask import abort, request, make_response, Response
import unicodedata
import copy
from math import radians, cos, sin, asin, sqrt


# Dados dois pontos no formato (latitude,longitude), calcula a distância de Haversine (distância entre dois pontos na superfície de uma esfera, no caso: a terra).
def haversine_dist(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance (in meters) between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine_dist formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    dist = 6367000 * c
    return dist

# Dado um conjunto de linhas e o cabecario, monta uma lista de dicionarios
def montaListaJson(spamreader, col):
    response = []
    colunas = col
    for row in spamreader:
        celulas = {}
        for indexColumns in range(0,len(colunas)):
            celulas[colunas[indexColumns]] = row[indexColumns]
        response.append(celulas)
    return response

# Dado uma lista de dicionarios retorna um JSON
def montaJson(response,sorted = False):
    return json.dumps(response,sort_keys=sorted,default=str).encode('utf8')

# Dado uma linha e o cabeçalho, monta um dicionario
def row_to_dict(row, columns):
    dict = {}
    for i in range(len(columns)):
        dict[columns[i]] = row[i]

    return dict

# Dada uma data, classifica que tipo de dia da semana é: dia útil(1), sábado(2) ou domingo(3)
def schedule_day_type(date):

    if (date_type(date)) == 1:
        day_type = "3"
    elif (date_type(date)) == 7:
        day_type = "2"
    else:
        day_type = "1"

    return day_type

# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios com todas as viagens daquela data
def get_travels(date,bus):
    query = "SELECT * FROM tb_viagem WHERE data = %s and rota = %s ORDER BY saida;"
    rows = bd.consulta(query, (date,bus))
    col=["id","rota","data","saida","chegada","duracao","numero_onibus","operador","id_bilhetagem"]
    return montaListaJson(rows, col)

# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios com todas as viagens daquela data
def get_travels_and_ticketing(date,bus):
    query = "SELECT v.rota,v.data,v.saida,v.chegada,v.duracao,v.numero_onibus,v.operador,b.passageiros,b.estudantes,b.gratuitos,b.equivalencia,v.stop_lat,v.stop_lon, v.initial_stop_id "\
    "FROM tb_viagem v, tb_bilhetagem b WHERE data = %s and rota = %s and v.id_bilhetagem = b.id ORDER BY saida;"
    rows = bd.consulta(query, (date,bus))
    col=["rota","data","saida","chegada","duracao","numero_onibus","operador","passageiros", "estudantes","gratuitos","equivalencia","stop_lat","stop_lon", "initial_stop_id"]
    return montaListaJson(rows, col)

def get_all_routes():
    query = "SELECT rota FROM tb_rota;"
    rows = bd.consulta(query)
    col=["rota"]
    return montaListaJson(rows, col)

# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios com todas as viagens daquela data
def get_travels_analysis(date,bus):
    query = "SELECT v.rota,v.data,v.saida,v.chegada,v.duracao,v.numero_onibus,v.operador,e.nome,l.nome, v.initial_stop_id FROM tb_viagem v, tb_onibus o, tb_empresa e, tb_rota r,tb_linha l "\
    "  WHERE v.data = %s and v.rota = %s and v.numero_onibus=o.numero and o.empresa=e.id and v.rota=r.rota and r.linha=l.id ORDER BY saida;"
    rows = bd.consulta(query, (date,bus))
    col=["rota","data","saida","chegada","duracao","numero_onibus","operador","nome_empresa", "nome_linha", "initial_stop_id"]
    return montaListaJson(rows, col)

# Dado retorna a última data que tem dados, uma lista de rotas e uma lista de dicionarios com todas as viagens daquela data
def get_all_travels(ranking_date):
    if ranking_date == "":
        query = "SELECT * FROM tb_viagem " \
                 "WHERE data = (SELECT MAX(data) FROM tb_data_rota) and " \
                 "rota IN (SELECT DISTINCT id_rota FROM tb_quadro_horario_2 WHERE id_rota != 'TIC-0001') " \
                 "ORDER BY rota, saida;"
    else:
        query = "SELECT * FROM tb_viagem " \
                 "WHERE data = '%s' and " \
                 "rota IN (SELECT DISTINCT id_rota FROM tb_quadro_horario_2 WHERE id_rota != 'TIC-0001') " \
                 "ORDER BY rota, saida;" % ranking_date
    rows = bd.consulta(query)
    cols = ["id","rota","data","saida","chegada","duracao","numero_onibus","operador","id_bilhetagem","initial_stop_id","stop_lat","stop_lon"]

    date = rows[0][2]

    routes_travels = {}
    routes = []

    for row in rows:
        route = row[1]

        if route not in routes_travels:
            routes_travels[route] = []
            routes.append(route)

        routes_travels[route].append(row_to_dict(row, cols))

    return date, routes, routes_travels

# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios da tabela da sttp sabendo se é dia útil, sábado ou domingo
def get_frame_schedules(date,bus):
    day_type = schedule_day_type(date)

    query = "SELECT qh.id, qh.tipo_dia, h.hora_onibus AS saida, ADDTIME(h.hora_onibus, SEC_TO_TIME(duracao)) AS chegada , qh.duracao, qh.tamanho_da_viagem, h.stop_lat, h.stop_lon, qh.id_rota, h.id_parada " \
            "FROM tb_quadro_horario_2 AS qh, tb_horario_quadro_horario AS h " \
            "WHERE qh.id = h.id_quadro_horario " \
            "AND qh.tipo_dia = %s " \
            "AND qh.id_rota = %s " \
            "AND h.indice_viagem = 1 " \
            "ORDER BY hora_onibus, duracao;"
    rows = bd.consulta(query, (day_type,bus))
    col=["id","tipo_dia","saida","chegada","duracao","tamanho_da_viagem","stop_lat","stop_lon","id_rota","id_parada"]

    return montaListaJson(rows, col)

# Dado uma data retorna um dicionário com as rotas e uma lista de dicionarios da tabela da sttp sabendo se é dia útil, sábado ou domingo
def get_all_frame_schedules(date):
    day_type = schedule_day_type(date)

    query = "SELECT qh.id, qh.tipo_dia, h.hora_onibus AS saida, ADDTIME(h.hora_onibus, SEC_TO_TIME(duracao)) AS chegada , qh.duracao, qh.tamanho_da_viagem, h.stop_lat, h.stop_lon, qh.id_rota, h.id_parada " \
            "FROM tb_quadro_horario_2 AS qh, tb_horario_quadro_horario AS h " \
            "WHERE qh.id = h.id_quadro_horario " \
            "AND qh.tipo_dia = %s " \
            "AND qh.id_rota IN (SELECT DISTINCT id_rota FROM tb_quadro_horario_2 WHERE id_rota != 'TIC-0001') " \
            "AND h.indice_viagem = 1 " \
            "ORDER BY id_rota, hora_onibus, duracao;"
    rows = bd.consulta(query, (day_type))
    cols = ["id","tipo_dia","saida","chegada","duracao","tamanho_da_viagem","stop_lat","stop_lon","id_rota","id_parada"]

    routes_schedules = {}

    for row in rows:
        route = row[8]

        if route not in routes_schedules:
            routes_schedules[route] = []

        routes_schedules[route].append(row_to_dict(row, cols))

    return routes_schedules

# transforma uma hora em segundos
def change_hour_second(hour):
    second = str(hour)[-8:].strip().split(':')
    return int(second[0]) * 3600 + int(second[1]) * 60 + int(second[2])

# transforma uma hora em minuto
def change_hour_minute(hour):
    return change_hour_second(hour)/60

def change_second_hour(second):
    return "%02d:%02d:%02d" % (int(second) / 3600, int(second) % 3600 / 60, int(second) % 3600 % 60)

# transforma uma hora em saida_ajuste, dada a função criada por Isabelle
def function_isabelle(hour):
    pIndex = 4 # Primeiro indice do grafico
    num = str(hour)[-8:].strip().split(':')
    num = int(str(num[0]))*60 + int(str(num[1])) - 60*pIndex
    return num

# Libera para teste com o localhost
def function_cors(data):
    response = data
    response = Response(response, status=200, mimetype='application/json')
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios com todas as viagens de datas anteriores daquela data
def get_travels_before_days(date,bus):
    query = "SELECT * FROM tb_viagem WHERE data < %s and rota = %s ORDER BY saida;"
    rows = bd.consulta(query, (date,bus))
    col=["id","rota","data","saida","chegada","duracao","numero_onibus","operador","id_bilhetagem"]
    return montaListaJson(rows, col)

# Checa se a rota nao possui viagens
def route_isEmpty(data,bus):
    query = "SELECT COUNT(*) FROM tb_viagem WHERE data < %s and rota = %s ORDER BY saida;"
    rows = bd.consulta(query, (data,bus))
    return function_cors(montaJson({"isEmpty": rows[0][0] == 0}))

# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios com uma média das viagens de datas anteriores daquela data
def get_median_before_date(data,bus):
    travels = get_travels_before_days(data,bus)

    return begin_end(travels)

# Dada uma data verifica qual dia da semana é: Domingo = 1, Segunda = 2,.
def date_type(date):
    return date_time(date).toordinal()%7 + 1

#Dada uma data retorna a data no formato datetime.date
def date_time(date):
    date = date.split("-")
    return datetime.date(int(date[0]),int(date[1]),int(date[2]))

# Dado duas datas e um onibus (4 digitos) retorna uma lista de dicionarios com todas as viagens entre essas duas datas com a data incial e sem a data final
def get_travels_between_days(date1,date2,bus):
    query = "SELECT * FROM tb_viagem WHERE data >= %s and data < %s and rota = %s ORDER BY saida;"
    rows = bd.consulta(query, (date1,date2,bus))
    col=["id","rota","data","saida","chegada","duracao","numero_onibus","operador","id_bilhetagem"]
    return montaListaJson(rows, col)

# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios com uma média das viagens de três dias antes daquela data
def get_median_between_tree_days(data,bus):
    date_beg = date_time(data)-datetime.timedelta(3)
    travels = get_travels_between_days(date_beg,data,bus)
    return begin_end(travels)


# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios com uma média das viagens da última semana
def get_median_last_week(data,bus):
    date_beg = date_time(data) - datetime.timedelta(6) - datetime.timedelta(date_type(data))
    date_end = date_time(data) - datetime.timedelta(date_type(data))
    travels = get_travels_between_days(date_beg,date_end,bus)
    return begin_end(travels)

# Dado uma data e um onibus (4 digitos) retorna uma lista de dicionarios com uma média das viagens dos três ultimos dias iguais
def get_median_tree_equals_days(data,bus):
    date_1 = date_time(data) - datetime.timedelta(7)
    date_2 = date_time(data) - datetime.timedelta(14)
    date_3 = date_time(data) - datetime.timedelta(21)
    travels = get_travels_tree_equals_days(date_1,date_2,date_3,bus)
    return begin_end(travels)

# Dado duas datas e um onibus (4 digitos) retorna uma lista de dicionarios com todas as viagens entre essas duas datas com a data incial e sem a data final
def get_travels_tree_equals_days(date1,date2,date3,bus):
    query = "SELECT * FROM tb_viagem WHERE (data = %s or data = %s or data = %s) and rota = %s ORDER BY saida;"
    rows = bd.consulta(query, (date1,date2,date3,bus))
    col=["id","rota","data","saida","chegada","duracao","numero_onibus","operador","id_bilhetagem"]
    return build_days_list(rows, col)

# Dado um conjunto de linhas e o cabecario, monta uma dicionário data: viagens
def build_days_list(rows, col):
    days = {}
    for row in rows:
        if row[2] not in days:
            days[row[2]] = []

        celulas = {}
        for indexColumns in range(0,len(col)):
            celulas[col[indexColumns]] = row[indexColumns]
        days[row[2]].append(celulas)

    return days

# Dado duas datas e um onibus (4 digitos) retorna uma lista de dicionarios com todas as viagens entre essas duas datas com a data incial e sem a data final
def get_days_travels_between_days(date1,date2,bus):
    query = "SELECT * FROM tb_viagem WHERE data >= %s and data < %s and rota = %s ORDER BY saida;"
    rows = bd.consulta(query, (date1,date2,bus))
    col=["id","rota","data","saida","chegada","duracao","numero_onibus","operador","id_bilhetagem"]
    return build_days_list(rows, col)

# Dado um quadro de horário, data inicial e final e um onibus retorna uma lista de lista de paireds
def list_of_paireds_same_type_days(frame_schedule, travels,date2, bus):
    days = []

    date_type2 = schedule_day_type(date2)

    if (len(travels) == 0):
        days.append(create_travels_comparison(travels, frame_schedule))

    for day in travels:

        formattedTime = datetime.datetime.strftime(day, "%Y-%m-%d")

        if (schedule_day_type(formattedTime) == date_type2):
            days.append(create_travels_comparison(travels[day], frame_schedule))

    return days

# Dado um quadro de horário, data inicial e final e um onibus retorna uma lista de lista de paireds
def list_of_paireds_same_type_days_usual_days(frame_schedule, travels,date2, bus):
    days = []

    if (len(travels) == 0):
        days.append(create_travels_comparison(travels, frame_schedule))

    for day in travels:

        formattedTime = datetime.datetime.strftime(day, "%Y-%m-%d")

        if (date_type(formattedTime) == 3 or date_type(formattedTime) == 4 or date_type(formattedTime) == 5):
            days.append(create_travels_comparison(travels[day], frame_schedule))

    return days

# Dado uma lista de lista de tuplas, retorna um dicionario, no qual a chave e o id de um frame_schedule
# e os valores sao [0] -> numero de vezes que esta viagem nao foi feita no periodo de tempo.
# [1] um array com as viagens que foram pareadas com esse frame_schedule
# [2] todos os dados do frame_schedule
def group_travels(paireds):
    dictionary = {"extra": []}
    for days in paireds:
        extra = 0
        for (travel, schedule) in days:
            if schedule is not None:
                if schedule["id"] not in dictionary.keys():
                    dictionary[schedule["id"]] = [0, [], schedule]

                if travel is None:
                    dictionary[schedule["id"]][0] += 1
                else:
                    dictionary[schedule["id"]][1].append(travel)
            else:
                extra += 1

        dictionary['extra'].append(extra)

    return dictionary


def get_median_tree_equals_days(frame_schedule, data,bus):
    date_1 = date_time(data) - datetime.timedelta(7)
    date_2 = date_time(data) - datetime.timedelta(14)
    date_3 = date_time(data) - datetime.timedelta(21)
    travels = get_travels_tree_equals_days(date_1,date_2,date_3,bus)

    paired_travels = list_of_paireds_same_type_days(frame_schedule, travels, data, bus)

    return group_travels(paired_travels)

def get_median_last_week(frame_schedule, data, bus):
    date_beg = date_time(data) - datetime.timedelta(6) - datetime.timedelta(date_type(data))
    date_end = date_time(data)


    travels = get_days_travels_between_days(date_beg, date_end, bus)

    paired_travels = list_of_paireds_same_type_days(frame_schedule, travels, data, bus)

    return group_travels(paired_travels)

# Dado um frame_schedule, uma data e um onibus, retorna a funcao group travels com as viagens de um mes
def get_median_typical(frame_schedule, date2, bus):
    date1 = date_time(date2) - datetime.timedelta(30)

    travels = get_days_travels_between_days(date1, date2, bus)

    paired_travels = list_of_paireds_same_type_days(frame_schedule, travels, date2, bus)

    return group_travels(paired_travels)

# Dado um frame_schedule, uma data e um onibus, retorna a funcao group travels com as viagens de um mes
def get_median_typical_usual_days(frame_schedule, date2, bus):
    date1 = date_time(date2) - datetime.timedelta(30)

    travels = get_days_travels_between_days(date1, date2, bus)

    paired_travels = list_of_paireds_same_type_days_usual_days(frame_schedule, travels, date2, bus)

    return group_travels(paired_travels)

# Dado um array e uma chave, retorna a mediana desse array de acordo com a chave
def median_for_comparisson(dict, key):
    if (len(dict) % 2 == 0):
        return (dict[len(dict) / 2][key] + dict[len(dict) / 2 - 1][key]) / 2
    else:
        return dict[len(dict) / 2][key]

# Retorna a mediana das viagens
def median_of_travels(group_travels, date, bus):

    delta_durations = []
    answer = []
    list_bus = []
    num_missing_travels = 0
    num_late_travels = 0
    num_travels = 0
    num_extra_travels = median(group_travels.pop("extra", None))

    for days in group_travels:
        if len(group_travels[days][1]) > 0:
            group_travels[days][1].sort(key=lambda item:item['saida'])
            saida = median_for_comparisson(group_travels[days][1], "saida")

            group_travels[days][1].sort(key=lambda item:item['chegada'])
            chegada = median_for_comparisson(group_travels[days][1], "chegada")

            duration = change_hour_minute(str(chegada-saida).split('.')[0])
            tb_duration = change_hour_minute(str(group_travels[days][2]["chegada"]-group_travels[days][2]["saida"]).split('.')[0])
            delta_duration = duration-tb_duration
            delta_durations.append(duration)
            answer.append({"rota":bus,
                "saida":str(saida).split('.')[0],
                "chegada":str(chegada).split('.')[0],
                "duracao":duration,
                "saida_tb":group_travels[days][2]["saida"],
                "chegada_tb":group_travels[days][2]["chegada"],
                "duracao_tb":tb_duration,
                "saida_ajuste":function_isabelle(str(saida).split('.')[0]),
                "saida_ajuste_tb":function_isabelle(str(group_travels[days][2]["saida"]).split('.')[0]),
                "del":delta_duration,
                "num_faltou": group_travels[days][0],
                "pareado": True,
                "tipo_viagem": "tolerado" if abs(delta_duration) < 30 else "atrasado"})

        else:
            num_missing_travels += 1
            tb_duration = change_hour_minute(str(group_travels[days][2]["chegada"]-group_travels[days][2]["saida"]).split('.')[0])
            duration = tb_duration
            delta_duration = duration-tb_duration
            answer.append({"rota":bus,
                "saida":str(group_travels[days][2]["saida"]).split('.')[0],
                "chegada":str(group_travels[days][2]["chegada"]).split('.')[0],
                "duracao":duration,
                "numero_onibus": "quadro_de_horario",
                "saida_tb":group_travels[days][2]["saida"],
                "chegada_tb":group_travels[days][2]["chegada"],
                "duracao_tb":tb_duration,
                "saida_ajuste":function_isabelle(str(group_travels[days][2]["saida"]).split('.')[0]),
                "del":delta_duration,
                "pareado": False,
                "tipo_viagem": "faltante"})

        if delta_duration >= 30 or delta_duration <= -30:
            num_late_travels += 1

    return function_cors(montaJson({"nodes" : answer, "num_late_travels": num_late_travels, "num_travels": num_travels, "median": median(delta_durations), "week_day": week_day(date),
    "num_extra_travels": num_extra_travels, "num_missing_travels": num_missing_travels, "list_bus" : list_bus}))


# Dado um json de viagens retorna uma lista de dicionarios com as médias dos horarios de saida e chegadas
def begin_end(travels):
    dictionary = {}
    for t in travels:
        if t["data"] in dictionary:
            dictionary[t["data"]].append(t)
        else:
            dictionary[t["data"]] = []

    list_final_begin = []
    list_final_end = []
    bigger = 0
    for v in dictionary.values():
        begin = []
        end = []
        for i in v:
            if (bigger < len(begin)):
                bigger = len(begin)
            begin.append(i["saida"])
            end.append(i["chegada"])
        list_final_begin.append(begin)
        list_final_end.append(end)

    list_final = []
    for i in range(bigger):
        begin = datetime.timedelta(0, 0)
        end = datetime.timedelta(0, 0)
        divisor = 0
        for l in range(len(list_final_begin)):
            try:
                begin = list_final_begin[l][i] + begin
                end = list_final_end[l][i] + end
                divisor = divisor+1
            except:
                pass
        list_final.append({"saida": (begin / divisor), "chegada": (end / divisor), "numero_onibus": travels[i]["numero_onibus"]})
    return list_final

# Para cada viagem feita, parear com o mais proximo da tabela
def create_travels_comparison(travels, frame_schedules):
    
    paireds = []

    if len(frame_schedules) == 0:
        for travel in travels:
            paireds.append((travel, None))
        return paireds

    headway = datetime.timedelta(minutes=30)

    for i in range(len(frame_schedules)):
        frame_schedules[i]["is_paired"] = False
        frame_schedules[i]["probably_paireds"] = []

        for j in range(len(travels)):
            travels[j]["is_paired"] = False

            if abs(frame_schedules[i]["saida"] - travels[j]["saida"]) <= headway:
				if haversine_dist(float(frame_schedules[i]["stop_lon"]),float(frame_schedules[i]["stop_lat"]),float(travels[j]["stop_lon"]),float(travels[j]["stop_lat"])) < 100:
					frame_schedules[i]["probably_paireds"].append(j)

    for schedule in frame_schedules:
        if len(schedule["probably_paireds"]) == 0:
            paireds.append((None, schedule))

        else:
            min_value = schedule["probably_paireds"][0]
            changed = False

            for index in schedule["probably_paireds"]:
				tdiff = abs(schedule["saida"] - travels[index]["saida"])
				min_tdiff = abs(schedule["saida"] - travels[min_value]["saida"])
				dist = haversine_dist(float(schedule["stop_lon"]),float(schedule["stop_lat"]),float(travels[index]["stop_lon"]),float(travels[index]["stop_lat"]))
				min_dist = haversine_dist(float(schedule["stop_lon"]),float(schedule["stop_lat"]),float(travels[min_value]["stop_lon"]),float(travels[min_value]["stop_lat"]))
				
				if not travels[index]["is_paired"] and  ((dist < min_dist) or (dist == min_dist and tdiff < min_tdiff)):
					min_value = index
					changed = True

            if changed:
                paireds.append((travels[min_value], schedule))
                schedule["is_paired"] = True
                travels[min_value]["is_paired"] = True
            else:
                paireds.append((None, schedule))

    for travel in travels:
        if not travel["is_paired"]:
            paireds.append((travel, None))

    for paired in paireds:
        if paired[1] is not None:
            del paired[1]["probably_paireds"]

    return paireds

# Para cada viagem feita, parear com o mais proximo da tabela
def create_travels_comparison_stop_id(travels, frame_schedules):
    
    paireds = []

    if len(frame_schedules) == 0:
        for travel in travels:
            paireds.append((travel, None))
        return paireds

    headway = datetime.timedelta(minutes=30)

    for i in range(len(frame_schedules)):
        frame_schedules[i]["is_paired"] = False
        frame_schedules[i]["probably_paireds"] = []

        for j in range(len(travels)):
            travels[j]["is_paired"] = False

            if abs(frame_schedules[i]["saida"] - travels[j]["saida"]) <= headway:
				if (frame_schedules[i]["id_parada"] == travels[j]["initial_stop_id"]):
					frame_schedules[i]["probably_paireds"].append(j)

    for schedule in frame_schedules:
        if len(schedule["probably_paireds"]) == 0:
            paireds.append((None, schedule))

        else:
            min_value = schedule["probably_paireds"][0]
            changed = False

            for index in schedule["probably_paireds"]:
				tdiff = abs(schedule["saida"] - travels[index]["saida"])
				min_tdiff = abs(schedule["saida"] - travels[min_value]["saida"])
				
				if not travels[index]["is_paired"] and  (tdiff <= min_tdiff):
					min_value = index
					changed = True

            if changed:
                paireds.append((travels[min_value], schedule))
                schedule["is_paired"] = True
                travels[min_value]["is_paired"] = True
            else:
                paireds.append((None, schedule))

    for travel in travels:
        if not travel["is_paired"]:
            paireds.append((travel, None))

    for paired in paireds:
        if paired[1] is not None:
            del paired[1]["probably_paireds"]

    return paireds

def median(list):
    list.sort()
    size = len(list)
    if size == 0:
        return 0
    elif size % 2 == 0:
        return (list[size/2] + list[size/2 - 1]) / 2.0
    else:
        return list[size/2]

def week_day(date):
    days = {1: 'Domingos', 2: 'Segundas-Feiras', 3: 'Terças-Feiras', 4: 'Quartas-Feiras', 5: 'Quintas-Feiras',
            6: 'Sextas-Feiras',7: 'Sábados'}
    return days[date_type(date)]

# Dado as viagens, o horario da tabela, uma data e um onibus (4 digitos) retorna um json usado no gráfico do site
def create_json_final_analysis(travels,frame_schedules,date,bus):

    answer = []

    paireds = create_travels_comparison(travels,frame_schedules)

    for paired in paireds:
        pair = False
        if paired[0] is None:
            tb_duration = change_hour_minute(str(paired[1]["chegada"]-paired[1]["saida"]).split('.')[0])
            duration = tb_duration
            delta_duration = duration-tb_duration

            saida = str(paired[1]["saida"]).split('.')[0]
            chegada = str(paired[1]["chegada"]).split('.')[0]
            numero_onibus = ""
            saida_tb = paired[1]["saida"]
            chegada_tb = paired[1]["chegada"]
            operador = ""
            nome_empresa = ""
            nome_linha = ""
        elif paired[1] is None:
            duration = change_hour_minute(str(paired[0]["chegada"]-paired[0]["saida"]).split('.')[0])
            tb_duration = duration
            delta_duration = duration-tb_duration

            saida = str(paired[0]["saida"]).split('.')[0]
            chegada = str(paired[0]["chegada"]).split('.')[0]
            numero_onibus = str(paired[0]["numero_onibus"]).split('.')[0]
            saida_tb = str(paired[0]["saida"])
            chegada_tb = str(paired[0]["chegada"])
            operador = unicodedata.normalize('NFKD', paired[0]["operador"]).encode('ascii', 'ignore')
            nome_empresa = str(paired[0]["nome_empresa"])
            nome_linha = unicodedata.normalize('NFKD', paired[0]["nome_linha"]).encode('ascii', 'ignore')
        else:
            pair = True
            duration = change_hour_minute(str(paired[0]["chegada"]-paired[0]["saida"]).split('.')[0])
            tb_duration = change_hour_minute(str(paired[1]["chegada"]-paired[1]["saida"]).split('.')[0])
            delta_duration = duration-tb_duration

            saida = str(paired[0]["saida"]).split('.')[0]
            chegada = str(paired[0]["chegada"]).split('.')[0]
            numero_onibus = str(paired[0]["numero_onibus"]).split('.')[0]
            saida_tb = str(paired[1]["saida"])
            chegada_tb = str(paired[1]["chegada"])
            operador = unicodedata.normalize('NFKD', paired[0]["operador"]).encode('ascii', 'ignore')
            nome_empresa = str(paired[0]["nome_empresa"])
            nome_linha = unicodedata.normalize('NFKD', paired[0]["nome_linha"]).encode('ascii', 'ignore')

            answer.append(("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n")%
                (bus,date,saida,chegada,duration,numero_onibus,saida_tb,chegada_tb,tb_duration,delta_duration,operador,nome_empresa,nome_linha,pair))

    return answer

# Dado as viagens, o horario da tabela, uma data e um onibus (4 digitos) retorna um json usado no gráfico do site
def create_json_final(travels,frame_schedules,date,bus):
    #paireds = create_travels_comparison(travels,frame_schedules)
    paireds = create_travels_comparison_stop_id(travels,frame_schedules)

    dict_final = create_dict_final(paireds,date,bus)

    return function_cors(montaJson(dict_final))


# Dado as viagens, o horario da tabela, uma data e um onibus (4 digitos) retorna um dict usado no gráfico do site
def create_dict_final(paireds,date,bus):

    num_late_travels = 0
    num_travels = 0
    num_extra_travels = 0
    num_missing_travels = 0
    delta_durations = []
    answer = []
    list_bus = []

    for paired in paireds:
        pair = False
        if paired[0] is None:
            num_missing_travels += 1
            tb_duration = change_hour_minute(str(paired[1]["chegada"]-paired[1]["saida"]).split('.')[0])
            duration = tb_duration
            delta_duration = duration-tb_duration
            answer.append({"rota":bus,
                "data":date,
                "saida":str(paired[1]["saida"]).split('.')[0],
                "chegada":str(paired[1]["chegada"]).split('.')[0],
                "duracao":duration,
                "numero_onibus": "quadro_de_horario",
                "saida_tb":paired[1]["saida"],
                "chegada_tb":paired[1]["chegada"],
                "duracao_tb":tb_duration,
                "saida_ajuste":function_isabelle(str(paired[1]["saida"]).split('.')[0]),
                "del":delta_duration,
                "pareado": pair,
                "tipo_viagem": "faltante"
                })

        elif paired[1] is None:
            duration = change_hour_minute(str(paired[0]["chegada"]-paired[0]["saida"]).split('.')[0])
            tb_duration = duration
            num_travels += 1
            num_extra_travels += 1
            delta_duration = duration-tb_duration
            delta_durations.append(duration)
            if (str(paired[0]["numero_onibus"]).split('.')[0] not in list_bus):
                list_bus.append(str(paired[0]["numero_onibus"]).split('.')[0])
            answer.append({"rota":bus,
                "data":date,
                "saida":str(paired[0]["saida"]).split('.')[0],
                "chegada":str(paired[0]["chegada"]).split('.')[0],
                "duracao":duration,
                "numero_onibus":str(paired[0]["numero_onibus"]).split('.')[0],
                "saida_tb":paired[0]["saida"],
                "chegada_tb":paired[0]["chegada"],
                "duracao_tb":tb_duration,
                "saida_ajuste":function_isabelle(str(paired[0]["saida"]).split('.')[0]),
                "del":delta_duration,
                "pareado": pair,
                "tipo_viagem": "extra",
                "ticketing": {"gratuitos": paired[0]["gratuitos"], "estudantes":paired[0]["estudantes"], "inteiros": paired[0]["passageiros"]-paired[0]["gratuitos"]-paired[0]["estudantes"], "equivalencia": float(paired[0]["equivalencia"])}})
        else:
            pair = True
            num_travels += 1
            duration = change_hour_minute(str(paired[0]["chegada"]-paired[0]["saida"]).split('.')[0])
            tb_duration = change_hour_minute(str(paired[1]["chegada"]-paired[1]["saida"]).split('.')[0])
            delta_duration = duration-tb_duration
            delta_durations.append(duration)
            if (str(paired[0]["numero_onibus"]).split('.')[0] not in list_bus):
                list_bus.append(str(paired[0]["numero_onibus"]).split('.')[0])
            answer.append({"rota":bus,
                "data":date,
                "saida":str(paired[0]["saida"]).split('.')[0],
                "chegada":str(paired[0]["chegada"]).split('.')[0],
                "duracao":duration,
                "numero_onibus":str(paired[0]["numero_onibus"]).split('.')[0],
                "saida_tb":paired[1]["saida"],
                "chegada_tb":paired[1]["chegada"],
                "duracao_tb":tb_duration,
                "saida_ajuste":function_isabelle(str(paired[0]["saida"]).split('.')[0]),
                "saida_ajuste_tb":function_isabelle(str(paired[1]["saida"]).split('.')[0]),
                "del":delta_duration,
                "pareado": pair,
                "tipo_viagem": "tolerado" if abs(delta_duration) < 30 else "atrasado",
                "ticketing": {"gratuitos": paired[0]["gratuitos"], "estudantes":paired[0]["estudantes"], "inteiros": paired[0]["passageiros"]-paired[0]["gratuitos"]-paired[0]["estudantes"], "equivalencia": float(paired[0]["equivalencia"])}})
            
        if delta_duration >= 30 or delta_duration <= -30:
            num_late_travels += 1

    return {"nodes" : answer, "num_late_travels": num_late_travels, "num_travels": num_travels, "median": median(delta_durations), "week_day": week_day(date), 
    "num_extra_travels": num_extra_travels, "num_missing_travels": num_missing_travels, "list_bus" : list_bus }


def get_valid_routes():
    query = "SELECT rota, data FROM tb_data_rota;"
    rows = bd.consulta(query)
    routes = {}
    for route in rows:
        routes[route[0]] = route[1]
    return montaJson({"routes": routes})

def delay_ranking(ranking_date):
    date, routes, routes_travels = get_all_travels(ranking_date)

    frames_schedules = get_all_frame_schedules(str(date))

    missing_frame_schedules = frames_schedules

    punctuality_percentages = []

    for route in routes:
        num_late_travels = 0
        num_missing_travels = 0
        num_extra_travels = 0
        paireds_length = 0
        punctual_travels = 0

        travels = routes_travels[route]
        try:
            frame_schedules = frames_schedules[route]
            del missing_frame_schedules[route]
        except:
            frame_schedules = []

            
        #paireds = create_travels_comparison(travels,frame_schedules)
        paireds = create_travels_comparison_stop_id(travels,frame_schedules)

        # deve ser colocado viagens a mais e a menos em um possível grafico de barra
        for i in range(len(paireds) - 1, -1, -1):
            if paireds[i][0] is None: #missing trip
                num_missing_travels += 1
                paireds.pop(i)

            elif paireds[i][1] is None: #extra trip
                num_extra_travels += 1
                paireds.pop(i)

            else:
                paireds_length += 1

                duration = change_hour_minute(str(paireds[i][0]["chegada"] - paireds[i][0]["saida"]).split('.')[0])
                tb_duration = change_hour_minute(str(paireds[i][1]["chegada"] - paireds[i][1]["saida"]).split('.')[0])
                delta_duration = duration-tb_duration

                if delta_duration >= 30 or delta_duration <= -30:
                    num_late_travels += 1
                else:
                    punctual_travels += 1

        if paireds_length != 0:
            punctuality_percentages.append({"route": route,
                                            "punctuality_percentage": punctual_travels / float(paireds_length) * 100,
                                            "number_of_delays": num_late_travels,
                                            "punctual_travels": punctual_travels,
                                            "total_of_paired_travels": paireds_length,
                                            "num_missing_travels": num_missing_travels,
                                            "num_missing_travels_percentage": paireds_length / float(len(frame_schedules)) * 100,
                                            "total_of_frame_schedule": len(frame_schedules),
                                            "num_extra_travels": num_extra_travels,
                                            "num_extra_travels_percentage": num_extra_travels / float(paireds_length + num_extra_travels) * 100
                                            })
        else:
            punctuality_percentages.append({"route": route,
                                            "punctuality_percentage": 100.0,
                                            "number_of_delays": 0,
                                            "punctual_travels": 0,
                                            "total_of_paired_travels": 0,
                                            "num_missing_travels": len(frame_schedules),
                                            "num_missing_travels_percentage": 0.0,
                                            "total_of_frame_schedule": len(frame_schedules),
                                            "num_extra_travels": len(travels),
                                            "num_extra_travels_percentage": 100.0
                                            })

    # for route in missing_frame_schedules.keys():
    #     punctuality_percentages.append({"route": route,
    #                                         "punctuality_percentage": 0.0,
    #                                         "number_of_delays": 0,
    #                                         "total_of_paired_travels": 0,
    #                                         "num_missing_travels": len(missing_frame_schedules),
    #                                         "num_missing_travels_percentage": 0.0,
    #                                         "total_of_frame_schedule": len(missing_frame_schedules),
    #                                         "num_extra_travels": 0,
    #                                         "num_extra_travels_percentage": 0
    #                                         })

    sorted_punctuality_percentages = sorted(punctuality_percentages, key=lambda k: k['punctuality_percentage'], reverse = True)

    return function_cors(montaJson({"date": date, "delays": sorted_punctuality_percentages, "bus_without_travel": missing_frame_schedules.keys()}))

def login(user, password):
    query = "SELECT * from tb_usuario WHERE nome=%s and senha=%s and funcao=1;"
    rows = bd.consulta(query, (user,password))
    if len(rows) == 0:
        return False
    else:
        return True

def get_route_trips_and_ticketing(start_date, end_date):
    answer = "id,passageiros,estudantes,gratuitos,equivalencia,id,rota,data,saida,chegada,duracao,numero_onibus,operador,id_bilhetagem,numero,empresa,id,nome\n"
    query = "SELECT * FROM tb_bilhetagem b, tb_viagem v, tb_onibus o, tb_empresa e WHERE b.id = v.id_bilhetagem AND v.numero_onibus = o.numero AND o.empresa = e.id AND v.data BETWEEN %s AND %s;"
    rows = bd.consulta(query, (start_date,end_date))
    for row in rows:
        id_bilhetagem = str(row[0])
        passageiros = row[1]
        estudantes = row[2]
        gratuitos = row[3]
        equivalencia = float(row[4])
        id_viagem = row[5]
        rota = str(row[6])
        data = datetime.datetime.strftime(row[7], '%Y-%m-%d')
        saida = str(row[8])
        chegada = str(row[9])
        duracao = row[10]
        numero_onibus = row[11]
        operador = row[12].encode('utf-8')
        id_bilhetagem2 = str(row[13])
        numero = row[14]
        empresa = str(row[15])
        id = str(row[16])
        nome = str(row[17])

        answer += ("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n") %\
                  (id_bilhetagem,passageiros,estudantes,gratuitos,equivalencia,id_viagem,rota,data,saida,chegada,duracao,numero_onibus,operador,id_bilhetagem2,numero,empresa,id,nome)

    return answer


def get_time_stocking_data(start_date, end_date):
    query = "SELECT SUM(b.passageiros),SUM(b.estudantes),SUM(b.gratuitos),SUM(b.equivalencia),v.data,e.nome  FROM tb_bilhetagem b, tb_viagem v, tb_onibus o, tb_empresa e WHERE b.id = v.id_bilhetagem AND v.numero_onibus = o.numero AND o.empresa = e.id AND e.nome != 'INDEFINIDO' AND v.data BETWEEN %s AND %s GROUP BY v.data, e.nome;"
    rows = bd.consulta(query, (start_date,end_date))

    col=["passageiros","estudantes","gratuitos","equivalencia","data","nome_empresa"]
    return montaListaJson(rows, col)


def time_stocking(ticketing_type,time_stocking_data, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    delta_days = (end_date - start_date).days + 1
    elements = {}

    initial_values = []
    start_time_stamp = time.mktime(start_date.timetuple())
    for i in range(delta_days):
        initial_values.append([start_time_stamp + i * 86400, 0])

    for stocking in time_stocking_data:
        if stocking["nome_empresa"] not in elements.keys():
            elements[stocking["nome_empresa"]] = {"key": stocking["nome_empresa"], "values": copy.deepcopy(initial_values)}

    for stocking in time_stocking_data:
        times = time.mktime(stocking["data"].timetuple())
        index = int((times - start_time_stamp) / 86400)
        elements[stocking["nome_empresa"]]["values"][index][1] = float(stocking[ticketing_type])

    return montaJson(elements.values())


def del_durations_day(year):
    answer = "rota,passageiros,estudantes,gratuitos,equivalencia,saida,chegada,saida_tb,chegada_tb,duracao,duracao_tb,delta_duration,delta_saida,data\n"

    routes = get_all_routes()
    for route in routes:
        print route
        frames_schedules = {}
        real_date = datetime.date(year, 1, 1)
        day = 0
        while (datetime.date(year, 12, 31) > real_date):
            real_date = real_date + datetime.timedelta(days=day)
            day = 1
            use_date = real_date.strftime("%Y-%m-%d")
            print use_date
            day_type = schedule_day_type(use_date)

            if day_type not in frames_schedules:
                frames_schedules[day_type] = get_frame_schedules(use_date,str(route["rota"]))

            frame_schedules = frames_schedules[day_type]

            travels = get_travels_and_ticketing(use_date,str(route["rota"]))
            paireds = create_travels_comparison(travels,frame_schedules)
            for paired in paireds:
                if not ((paired[0] is None) or (paired[1] is None)):
                    duration = paired[0]["duracao"]
                    tb_duration = paired[1]["duracao"]
                    delta_duration = duration-tb_duration

                    delta_exit = change_hour_minute(str(paired[0]["saida"]).split('.')[0]) - change_hour_minute(str(paired[1]["saida"]).split('.')[0])

                    rota = route["rota"]
                    passageiros = paired[0]["passageiros"]
                    estudantes = paired[0]["estudantes"]
                    gratuitos = paired[0]["gratuitos"]
                    equivalencia = paired[0]["equivalencia"]
                    saida = paired[0]["saida"]
                    chegada = paired[0]["chegada"]
                    saida_tb = paired[1]["saida"]
                    chegada_tb =paired[1]["chegada"]
                    if chegada_tb.days != 0:
                        chegada_tb = str(chegada_tb.seconds // 3600)+":"+str(chegada_tb.seconds // 60 % 60)+":"+str(chegada_tb.seconds)
                    if chegada.days != 0:
                        chegada = str(chegada.seconds // 3600)+":"+str(chegada.seconds // 60 % 60)+":"+str(chegada.seconds)


                    answer += ("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n") %\
                      (rota,passageiros,estudantes,gratuitos,equivalencia,saida,chegada,saida_tb,chegada_tb,duration,tb_duration,delta_duration,delta_exit,use_date)

    f = open('analises2015.csv','w')
    f.write(answer)
    f.close()

    return answer
