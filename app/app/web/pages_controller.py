from flask import Blueprint, render_template
from flask_login import login_required

pages_blueprint = Blueprint('pages', __name__)

@pages_blueprint.route('/')
@login_required
def home():
    return render_template('home/index.html')

@pages_blueprint.route('/about')
def about():
    return render_template('about/index.html')

@pages_blueprint.route('/ponto-de-venda/index.html')
@login_required
def ponto_de_venda():
    return render_template('Ponto_de_venda/index.html')

@pages_blueprint.route('/produtos/index.html')
@login_required
def produtos():
    return render_template('produto/index.html')

@pages_blueprint.route('/clientes/index.html')
@login_required
def clientes():
    return render_template('clientes/index.html')
