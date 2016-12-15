#!flask/bin/python
# -*- coding: utf-8 -*-

import bd
from flask import jsonify, session


def resposta_sucesso(mensagem):
    m = {'mensagem':mensagem}
    return jsonify(m)


def is_authenticated():
    return 'matricula' in session

def login(matricula, senha):
    query = "SELECT * FROM tb_usuario WHERE matricula=%s AND senha=%s"
    row = bd.consulta(query, (matricula, senha))
    if len(row) > 0:
        user = row[0]
        if user[5] == 1:
            session['matricula'] = user[1]
            session['nome'] = user[2]
            session['funcao'] = user[4]

def logout():
    keys = ['matricula', 'nome', 'funcao']
    for e in keys:
        session.pop(e)
