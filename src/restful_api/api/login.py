import json
import util
from api import app
from flask import make_response, redirect, render_template, request, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)

        matricula = data['matricula']
        senha = data['senha']

        return do_login(matricula, senha)

    if util.is_authenticated():
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    util.logout()

    return redirect(url_for('index'))

def do_login(matricula, senha):
    util.login(matricula, senha)

    if util.is_authenticated():
        return make_response(json.dumps(True))
    else:
        return make_response(json.dumps(False))
