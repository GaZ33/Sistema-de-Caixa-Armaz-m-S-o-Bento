from flask import render_template, redirect, url_for, request, session, flash, Blueprint, jsonify, abort, send_from_directory, current_app
from app import app

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def index():
    return render_template('base_template.html')