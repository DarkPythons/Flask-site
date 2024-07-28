from flask import Blueprint, render_template, request, flash, redirect, url_for
from .auth_orm import OrmRequest
from flask_login import current_user


router_auth = Blueprint('router_auth', __name__, static_folder='static', template_folder='templates')



@router_auth.route('/login', methods=['POST', 'GET'])
def login():
    orm = OrmRequest()
    #Если пользователь уже авторизован
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    #Доделать.
    if request.method == 'POST':
        user = orm.get_user_by_email(request.form['email'])
        print(user)

    return render_template('auth/login.html', title='Вход')

def data_validate(form_data):
    if len(form_data['username']) > 3 and len(form_data['email']) > 5 and "@" in form_data['email']:
        if form_data['psw'] == form_data['psw2']:
            return 200
        else:
            return 401
    else:
        return 400

@router_auth.route('/register', methods=['POST', 'GET'])
def register():
    orm = OrmRequest()
    if request.method == 'POST':
        if data_validate(request.form) == 200:
            try:
                orm.register_user(request.form['username'], request.form['email'], request.form['psw'])
            except Exception as error:
                #Откат базы данных в случае ошибки
                orm.get_rollback()
                flash('Ошибка на стороне базы данных')
                print('Ошибка на стороне базы данных: ' + str(error))
        elif data_validate(request.form) == 400:
            flash("Неккоректные email или username", category='error')
        else:
            flash('Пароли не совпадают.', category='error')

    return render_template('auth/register.html', title='Регистрация')

@router_auth.route('/profile', methods=['GET'])
def profile():
    return "Ваш профиль"