from flask import render_template, Blueprint

router_main = Blueprint("router_main", __name__, static_folder='static', template_folder='templates')

@router_main.route('/')
def index():
    return render_template('index.html', title='Главная страница')

@router_main.route('/about')
def about():
    return render_template('about.html', title='О нас')

