from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user

from .auth_orm import OrmRequest
from .UserLogin import UserLogin
from .utils import data_validate, creating_dict_for_profile



router_auth = Blueprint('router_auth', __name__, static_folder='static', template_folder='templates')


def create_user_session(*, user):
    """Фукнция для создания сессии пользователю по данным из бд 
    (используется при регистрации, входа в аккаунт)
    """
    userLogin = UserLogin().create(user)
    rm = True if request.form.get('remainme') else False
    login_user(userLogin, remember=rm)
    return redirect(url_for('.profile'))    


def function_by_login():
    """Функция для обработки данных и создания сессии, когда пользователь выполнял аунтефикацию"""
    orm = OrmRequest()
    user_from_orm = orm.get_user_by_email(request.form['email'])
    if user_from_orm:
        password_valid = orm.validate_password_user(user_from_orm['psw'], request.form['psw'])
        if password_valid:
            create_user_session(user=user_from_orm)
        else:
            flash('Неверная пара email/пароль', category='error')
    else:
        flash('Неверная пара email/пароль', category='error')

def function_by_register():
    """Функция для обработки данных и создания сессии, когда пользователь выполнял 
    регистрацию аккаунта
    """
    orm = OrmRequest()
    try:
        user = orm.get_user_by_email(request.form['email'])
        if not user:
            orm.register_user(request.form['username'], request.form['email'], request.form['psw'])
            #Получение пользователя из базы по его email и создание 
            user_from_orm = orm.get_user_by_email(request.form['email'])
            create_user_session(user=user_from_orm)
        else:
            flash('Пользователь с таким email уже есть.', category='error')
    except Exception as error:
        #Откат базы данных в случае ошибки
        orm.get_rollback()
        flash('Ошибка на стороне базы данных', category='error')

@router_auth.route('/login', methods=['POST', 'GET'])
def login():
    #Если пользователь уже авторизован
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))
    if request.method == 'POST':
        function_by_login()
    return render_template('auth/login.html', title='Вход')



@router_auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))
    if request.method == 'POST':
        if data_validate(request.form) == 200:
            function_by_register()
        elif data_validate(request.form) == 400:
            flash("Неккоректные email или username", category='error')
        else:
            flash('Пароли не совпадают.', category='error')
    return render_template('auth/register.html', title='Регистрация')

@login_required
@router_auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", category='success')
    return redirect(url_for('.login'))


@login_required
@router_auth.route('/profile', methods=['GET'])
def profile(): 
    orm = OrmRequest()
    user_email = current_user.get_email()
    user_info = orm.get_user_by_email(user_email)
    date: dict = creating_dict_for_profile(user_info)
    return render_template('auth/profile.html', title='Профиль', date=date)
