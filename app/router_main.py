"""
Модуль, в котором лежат основные страницы сайта по базову url
index: главная страницa сайта
about: страница 'о нас'
"""
from flask import render_template, Blueprint

main_router = Blueprint("main_router", __name__, 
    static_folder='static', 
    template_folder='templates')

@main_router.route('/')
def index():
    """Обработчик запроса на главную страницу"""
    return render_template('index.html', title='Главная страница')

@main_router.route('/about')
def about():
    """Обработчик запроса страницы 'о нас'."""
    return render_template('about.html', title='О нас')