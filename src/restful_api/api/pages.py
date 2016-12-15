import util
from api import app
from flask import render_template
from flask_auth.authentication import RequiresAuthentication

@app.route('/')
@RequiresAuthentication(util.is_authenticated, 'login')
def index():
    return render_template('index.html')


@app.route('/todas_escalas/')
@RequiresAuthentication(util.is_authenticated, 'login')
def todas_escalas():
    return render_template('escalas.html')


@app.route('/escalas/')
@RequiresAuthentication(util.is_authenticated, 'login')
def escalas():
    return render_template('tables.html')


@app.route('/painel/')
@RequiresAuthentication(util.is_authenticated, 'login')
def painel_controle():
    return render_template('forms.html')