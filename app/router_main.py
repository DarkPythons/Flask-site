from flask import render_template, Blueprint

router = Blueprint("router", __name__, static_folder='static', template_folder='templates')

@router.route('/')
def index():
    return render_template('index.html', title='Главная страница')

@router.route('/about')
def about():
    return render_template('about.html', title='О нас')

