# -*- coding: utf-8 -*-
import bd
import json
import util
from api import app
from flask import abort, request


@app.route('/api/v1/count/')
def api_v1_get_numero_usuarios():
    query = "SELECT COUNT(*) FROM tb_usuario;"
    row = bd.consulta(query)
    return str(row[0][0])


@app.route('/api/v1/usuarios/', methods=['GET'])
def api_v1_usuarios():
    query = "SELECT * FROM tb_usuario;"
    row = bd.consulta(query)
    return json.dumps(row)


@app.route('/api/v1/usuarios/<int:matricula>/', methods=['GET'])
def api_v1_mostrar_usuario(matricula):
    query = "SELECT * FROM tb_usuario WHERE matricula = %s;"
    row = bd.consulta(query, (matricula,))
    if row:
        return json.dumps(row)
    else:
        abort(404)


@app.route('/api/v1/usuarios/<int:matricula>/alocacoes/', methods=['GET'])
def api_v1_get_alocacoes_usuario(matricula):
    query = "SELECT * FROM tb_alocacao WHERE id_usuario = %s;"
    row = bd.consulta(query, (matricula,))
    if row:
        return json.dumps(row)
    else:
        abort(404)


@app.route('/api/v1/usuarios/', methods=['POST'])
def api_v1_criar_usuario():
    query = "INSERT INTO tb_usuario (matricula, nome, senha, funcao) VALUES (%s, %s, %s, %s);"
    matricula = int(request.json['matricula'])
    nome = request.json.get("nome", "")
    senha = request.json.get("senha", "")
    funcao = int(request.json['funcao'])
    argumentos = (matricula, nome, senha, funcao)
    if bd.insere(query, argumentos):
        return util.resposta_sucesso("Usuario criado com sucesso")
    else:
        abort(404)


@app.route('/api/v1/escalas/', methods=['GET'])
def api_v1_mostrar_escalas():
    query = "SELECT tb_escala.id, tb_escala.mes, tb_escala.ano, tb_turno_escala.turno, tb_status_escala.status FROM tb_escala, tb_turno_escala, tb_status_escala WHERE tb_escala.turno = tb_turno_escala.id AND tb_escala.status = tb_status_escala.id;"
    row = bd.consulta(query)
    if row:
        return json.dumps(row)
    else:
        abort(404)


@app.route('/api/v1/escalas/<int:id>/', methods=['GET'])
def api_v1_mostrar_escala(id):
    query = "SELECT * FROM tb_escala WHERE id = %s;"
    row = bd.consulta(query, (id,))
    if row:
        return json.dumps(row)
    else:
        abort(404)


@app.route('/api/v1/escalas/<int:id>/turno/', methods=['GET'])
def api_v1_get_turno(id):
    query = "SELECT turno FROM tb_escala WHERE id = %s"
    row = bd.consulta(query, (id,))
    if row:
        return json.dumps([row[0]])
    else:
        abort(500)


@app.route('/api/v1/escalas/', methods=['POST'])
def api_v1_criar_escala():
    query = "INSERT INTO tb_escala (mes, ano, turno, status) VALUES (%s, %s, %s, %s);"
    mes = int(request.json['mes'])
    ano = int(request.json['ano'])
    turno = int(request.json['turno'])
    status = 1 #1: Não-aprovado
    argumentos = (mes, ano, turno, status)
    if bd.insere(query, argumentos):
        return util.resposta_sucesso("Escala criada com sucesso!")
    else:
        abort(500)


@app.route('/api/v1/escalas/<int:id>/turno/', methods=['PATCH'])
def api_v1_set_turno(id):
    query = "UPDATE tb_escala SET turno = %s WHERE id = %s;"
    turno = int(request.json['value'])
    if bd.atualiza(query, (turno, id)):
        return util.resposta_sucesso("Alterações realizadas com sucesso")
    else:
        abort(500)


@app.route('/api/v1/escalas/<int:id>/', methods=['DELETE'])
def api_v1_remover_escala(id):
    if __remover_todas_alocacoes(id):
        query = "DELETE FROM tb_escala WHERE id = %s;"
        if bd.remove(query, (id,)):
            return util.resposta_sucesso("Escala removida com sucesso!")
        else:
            abort(500)
    else:
        abort(500)


@app.route('/api/v1/escalas/<int:id_escala>/alocacoes/', methods=['GET'])
def api_v1_mostrar_alocacao(id_escala):
    query = "SELECT tb_usuario.nome, tb_ponto_de_fiscalizacao.nome, tb_alocacao.dia, tb_escala.mes FROM tb_usuario, tb_ponto_de_fiscalizacao, tb_alocacao, tb_escala WHERE tb_alocacao.id_escala = %s AND tb_alocacao.id_escala = tb_escala.id AND tb_alocacao.id_ponto_fiscalizacao = tb_ponto_de_fiscalizacao.id AND tb_usuario.matricula = tb_alocacao.id_usuario;"
    row = bd.consulta(query, (id_escala,))
    if row:
        return json.dumps(row)
    else:
        abort(404)


@app.route('/api/v1/escalas/<int:id_escala>/alocacoes/', methods=['POST'])
def api_v1_adicionar_alocacoes(id_escala):
    '''Este método adiciona um conjunto de alocações a determinada escala.
    Note-se que o id da escala é passado na URL.
    Ele espera, como request, um JSON no seguinte formato:

    {
        "1":{
            "id_usuario" = <int> matricula,
            "id_ponto_fiscalizacao" = <int> id_ponto,
            "dia": <int> dia_da_semana
            },
        "2":{
            "id_usuario" = <int> matricula,
            "id_ponto_fiscalizacao" = <int> id_ponto,
            "dia": <int> dia_da_semana
            }
    }
    '''

    sucesso = True
    for key in request.json:
        query = "INSERT INTO tb_alocacao (id_usuario, id_ponto_fiscalizacao, dia, id_escala) VALUES (%s, %s, %s, %s);"
        usuario = int(request.json[key]['id_usuario'])
        ponto_fiscalizacao = int(request.json[key]['id_ponto_fiscalizacao'])
        dia = int(request.json[key]['dia'])
        escala = id_escala
        argumentos = (usuario, ponto_fiscalizacao, dia, escala)
        if not bd.insere(query, argumentos):
            sucesso = False
    if sucesso:
        return util.resposta_sucesso("Operação realizada com sucesso")
    abort(500)


@app.route('/api/v1/escalas/alocacoes/<int:id>/', methods=['DELETE'])
def api_v1_remover_alocacao(id):
    query = "DELETE FROM tb_alocacao WHERE id = %s;"
    if bd.remove(query, (id,)):
        return util.resposta_sucesso("Alocação removida com sucesso!")
    else:
        abort(500)


@app.route('/api/v1/pontos_de_fiscalizacao/', methods=['GET'])
def api_v1_pontos_de_fiscalizacao():
    query = "SELECT * FROM tb_ponto_de_fiscalizacao;"
    row = bd.consulta(query)
    return json.dumps(row)


def __remover_todas_alocacoes(id_escala):
    query = "DELETE FROM tb_alocacao WHERE id_escala = %s;"
    if bd.remove(query, (id_escala,)):
        return True
    else:
        return False