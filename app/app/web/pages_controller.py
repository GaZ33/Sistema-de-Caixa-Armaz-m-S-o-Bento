from flask import Blueprint, render_template

pages_blueprint = Blueprint('pages', __name__)

@pages_blueprint.route('/')
def home():
    return render_template('home/index.html')

@pages_blueprint.route('/about')
def about():
    return render_template('about/index.html')