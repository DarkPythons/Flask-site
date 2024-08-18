from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user

from .auth_orm import OrmRequest
from .UserLogin import UserLogin
from .utils import data_validate, creating_dict_for_profile



router_auth = Blueprint('router_auth', 
    __name__, 
    static_folder='static', 
    template_folder='templates'
    )


def create_user_session(*, user):
    """Фукнция для создания сессии пользователю по данным из бд 
    (используется при регистрации, входа в аккаунт)
    """
    userLogin = UserLogin().create(user)
    rm = True if request.form.get('remainme') else False
    login_user(userLogin, remember=rm)
    return 200


def function_by_login():
    """Функция для обработки данных и создания сессии, когда пользователь выполнял аунтефикацию"""
    orm = OrmRequest()
    user_from_orm = orm.get_user_by_email(request.form['email'])
    if user_from_orm:
        password_valid = orm.validate_password_user(user_from_orm['psw'], request.form['psw'])
        if password_valid:
            result = create_user_session(user=user_from_orm)
            return result
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
            result = create_user_session(user=user_from_orm)
            return result
        else:
            flash('Пользователь с таким email уже есть.', category='error')
    except Exception as error:
        #Откат базы данных в случае ошибки
        orm.get_rollback()
        flash('Ошибка на стороне базы данных', category='error')

@router_auth.route('/login', methods=['POST', 'GET'])
def login():
    """
    Обработчик запроса на получение страницы аутентификации и обработчик
    данных с формы, которую заполняет пользователь (mail, psw), при корректных данных,
    выдает сессию и возвращает redirect на профиль пользователя.
    """
    #Если пользователь уже авторизован
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))
    if request.method == 'POST':
        result = function_by_login()
        if result == 200:
            return redirect(url_for('.profile'))
    return render_template('auth/login.html', title='Вход')



@router_auth.route('/register', methods=['POST', 'GET'])
def register():
    """
    Обработчик запроса на получение страницы регистрации и обработка данных с формы, 
    полученных со страницы (username, mail, psw1, psw2), при валидных данных выдает
    сессию пользователю и перекидывает его на профиль.
    """
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))
    if request.method == 'POST':
        if data_validate(request.form) == 200:
            result = function_by_register()
            if result == 200:
                return redirect(url_for('.profile'))
        elif data_validate(request.form) == 400:
            flash("Неккоректные email или username", category='error')
        else:
            flash('Пароли не совпадают.', category='error')
    return render_template('auth/register.html', title='Регистрация')

@login_required
@router_auth.route('/logout', methods=['GET'])
def logout():
    """
    Обработчик запроса на выход из аккаунта, доступен тем пользователям, 
    у которых есть сессия. 
    Забирает сессию у пользователя и возвращает redirect на url функции аутентификации.
    """
    logout_user()
    flash("Вы вышли из аккаунта", category='success')
    return redirect(url_for('.login'))


@login_required
@router_auth.route('/profile', methods=['GET'])
def profile():
    """
    Получение своего профиля, доступен только пользователям с сессией.
    Формирует данные о пользователе и возвращает их в html странице.
    """
    orm = OrmRequest()
    user_email = current_user.get_email()
    user_info = orm.get_user_by_email(user_email)
    date: dict = creating_dict_for_profile(user_info)
    return render_template('auth/profile.html', title='Профиль', date=date)
