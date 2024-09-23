"""
Модуль, который содержит обработчики запросов для входа/регистрации/обновления данных профиля
login: Получение формы для входа в профиль и её обработка
register: Получение формы для регистрации и её обработка
logout: Сделать выход из своего аккаунта
profile: Получить свой профиль
edit_profile: Получение формы для изменения своего профиля и обработка этой формы
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_required, logout_user

from .auth_orm import AuthOrm
from .utils import (data_validate, creating_dict_for_profile, function_by_login, 
    function_by_register, edit_profile_funtion
    )

auth_router = Blueprint('router_auth', 
    __name__, 
    static_folder='static', 
    template_folder='templates'
    )

@auth_router.route('/login', methods=['POST', 'GET'])
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

@auth_router.route('/register', methods=['POST', 'GET'])
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

@auth_router.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Обработчик запроса на выход из аккаунта, доступен тем пользователям, 
    у которых есть сессия. 
    Забирает сессию у пользователя и возвращает redirect на url функции аутентификации.
    """
    logout_user()
    session.clear()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']
    flash("Вы вышли из аккаунта", category='success')
    return redirect(url_for('.login'))

@auth_router.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    Получение своего профиля, доступен только пользователям с сессией.
    Формирует данные о пользователе и возвращает их в html странице.
    """
    orm = AuthOrm()
    user_email = current_user.get_email()
    user_info = orm.get_user_by_email(user_email)
    try:
        date: dict = creating_dict_for_profile(user_info)
    except TypeError as Error:
        return redirect(url_for('.logout'))
    return render_template('auth/profile.html', title='Профиль', date=date)

@auth_router.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Получение страницы для редактирования своего профиля
    и обработка отправленной формы новых данных для профиля.
    """
    orm = AuthOrm()
    user_email = current_user.get_email()
    user_info = orm.get_user_by_email(user_email)
    if request.method == 'POST':
        status_update = edit_profile_funtion(orm, user_info)
        if status_update == 200:
            return redirect(url_for('.profile'))
        else:
            pass
    return render_template('auth/edit_profile.html', title='Редактирование профиля', user_data=user_info)