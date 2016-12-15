#!flask/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
from config import Config


def conexao():
    config = Config()
    return MySQLdb.connect(config.get_db_host(), config.get_db_user(), config.get_db_passwd(), config.get_db_name(),
        config.get_db_port(), charset="utf8")


def consulta(query, argumentos=None):
    return __executa_query(query, argumentos)


def insere(query, argumentos=None):
    return __executa_query(query, argumentos, commit=True)


def atualiza(query, argumentos=None):
    return __executa_query(query, argumentos, commit=True)


def remove(query, argumentos=None):
    return __executa_query(query, argumentos, commit=True)


def __executa_query(query, argumentos=None, commit=False):
    if query:
        con = conexao()
        cursor = con.cursor()
        if argumentos:
            cursor.execute(query, argumentos)
        else:
            cursor.execute(query)
        if commit:
            return __commit(con)
        else:
            resultados = cursor.fetchall()
            cursor.close()
            return resultados


def __commit(conexao):
    done = True
    try:
        conexao.commit()
    except Exception, e:
        done = False
        conexao.rollback()
        print e
    return done