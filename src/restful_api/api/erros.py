#!flask/bin/python
# -*- coding: utf-8 -*-

from api import app
from flask import jsonify, make_response


@app.errorhandler(401)
def unauthorized(error=None):
    mensagem = {'status': 401, 'mensagem': 'Voce nao tem permissao para acessar essa pagina!'}
    resp = jsonify(mensagem)
    resp.status_code = 401
    # REDIRECIONAR PRO LOGIN
    return resp


@app.errorhandler(404)
def not_found(error=None):
    mensagem = {"status": 404, "mensagem": 'Nao encontramos o que voce estava procurando. Tente novamente.'}
    resp = jsonify(mensagem)
    resp.status_code = 404
    return resp


@app.errorhandler(405)
def method_not_allowed(error=None):
    mensagem = {'status': 405, 'mensagem': 'Metodo nao permitido!'}
    resp = jsonify(mensagem)
    resp.status_code = 405
    return resp


@app.errorhandler(500)
def internal_server_error(error=None):
    mensagem = {'status': 500, 'mensagem': 'Ops. Algo deu errado. Tente novamente.'}
    resp = jsonify(mensagem)
    resp.status_code = 500
    return resp