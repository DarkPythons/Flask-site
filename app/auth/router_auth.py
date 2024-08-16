from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, login_required

from .auth_orm import OrmRequest
from .UserLogin import UserLogin
from .utils import data_validate

router_auth = Blueprint('router_auth', __name__, static_folder='static', template_folder='templates')



@router_auth.route('/login', methods=['POST', 'GET'])
def login():
    orm = OrmRequest()
    #Если пользователь уже авторизован
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))
    if request.method == 'POST':
        user = orm.get_user_by_email(request.form['email'])
        if user:
            user = user[0]
            password_valid = orm.validate_password_user(user['psw'], request.form['psw'])
            if password_valid:
                userLogin = UserLogin().create(user)
                rm = True if request.form.get('remainme') else False
                login_user(userLogin, remember=rm)
                return redirect(url_for('.profile'))
            else:
                flash('Неверная пара email/пароль', category='error')
        else:
            flash('Неверная пара email/пароль', category='error')
    return render_template('auth/login.html', title='Вход')



@router_auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))
    orm = OrmRequest()
    if request.method == 'POST':
        if data_validate(request.form) == 200:
            try:
                user = orm.get_user_by_email(request.form['email'])
                if not user:
                    orm.register_user(request.form['username'], request.form['email'], request.form['psw'])

                    return redirect(url_for('.profile'))
                else:
                    flash('Пользователь с таким email уже есть.', category='error')
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
@login_required
def profile():
    return "Ваш профиль"