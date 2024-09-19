from flask import render_template, Blueprint, send_from_directory
import os

main_router = Blueprint("main_router", __name__, 
    static_folder='static', 
    template_folder='templates')

@main_router.route('/')
def index():
    return render_template('index.html', title='Главная страница')

@main_router.route('/about')
def about():
    return render_template('about.html', title='О нас')


@main_router.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join('app', 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')