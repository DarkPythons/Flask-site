"""
Модуль для вынесения разных функций из основной программы,
для улучшения читабельности.
data_validate: проводит валидацию данных из формы регистрации
"""
from flask import request, flash
from flask_login import login_user

from .UserLogin import UserLogin
from .auth_orm import AuthOrm
from base_log import log_app, log_except

def data_validate(form_data):
    """
    Проводит валидацию данных из формы регистрации, 
    если все данные будут корректны, вернется статус 200
    form_data: данные из формы, которые ввел пользователь
    """
    if len(form_data['username']) > 3 and len(form_data['email']) > 5 and "@" in form_data['email']:
        if form_data['psw'] == form_data['psw2']:
            return 200
        else:
            return 401
    else:
        return 400
    

def creating_dict_for_profile(user_orm: dict) -> dict:
    """
    Создание dict с нужными данными на основании данных из базы,
    которые мы отдадим на фронтенд, где уже будет страница с профилем пользователя
    user_orm: содержит dict, в котором указаны данные о пользователе
    """
    date = {
        "username" : user_orm['username'],
        "email" : user_orm['email'],
        "date" : user_orm['date'],
        "about" : user_orm['about']
    }
    return date

def create_user_session(*, user):
    """
    Фукнция для создания сессии пользователю по данным из бд 
    (используется при регистрации, входа в аккаунт)
    user: данные из базы, на основании которых будет создан пользователь (сессия)
    """
    userLogin = UserLogin().create(user)
    rm = True if request.form.get('remainme') else False
    login_user(userLogin, remember=rm)
    return 200


def function_by_login():
    """
    Функция, которая проверяет данные из формы входа на корректность, после чего, если данные
    пользователя верны, выдает ему сессию
    """
    orm = AuthOrm()
    user_from_orm = orm.get_user_by_email(request.form['email'])
    if user_from_orm:
        password_valid = orm.validate_password_user(user_from_orm['psw'], request.form['psw'])
        if password_valid:
            log_app.info(f'Пользовать с id {user_from_orm['id']} вошел в аккаунт.')
            result = create_user_session(user=user_from_orm)
            return result
        else:
            flash('Неверная пара email/пароль', category='error')
    else:
        flash('Неверная пара email/пароль', category='error')

def function_by_register():
    """
    Функция для обработки данных из формы регистрации, если данные корректны, сессия будет выдана,
    а аккаунт создан
    """
    orm = AuthOrm()
    try:
        user = orm.get_user_by_email(request.form['email'])
        if not user:
            orm.register_user(request.form['username'], request.form['email'], request.form['psw'])
            #Получение пользователя из базы по его email и создание 
            user_from_orm = orm.get_user_by_email(request.form['email'])
            result = create_user_session(user=user_from_orm)
            log_app.info(f'Пользователь с id {user_from_orm['id']} из базы зарегистрировался')
            return result
        else:
            flash('Пользователь с таким email уже есть.', category='error')
    except Exception as Error:
        #Откат базы данных в случае ошибки
        orm.get_rollback()
        log_except.error(f'Ошибка при регистрации пользователя: {Error}')
        flash('Ошибка на стороне базы данных', category='error')


def edit_profile_funtion(orm: AuthOrm, user_info: dict):
    """
    Функция для обработки данных из формы обновления профиля
    orm: объект, который позволяет взаимодействовать с таблицей пользователей
    user_info: информация из базы данных о пользователе
    """
    status_code = 200
    try:
        new_username = request.form['username']
        new_about = request.form['about']
        orm.update_data_user(new_username=new_username, new_about=new_about, user_id=user_info['id'])
        flash('Изменение данных аккаунта прошло успешно', category='success')   
    except Exception as Error:
        log_except.error(f'Ошибка при изменении данных профиля: {Error}')
        flash('Ошибка при изменении данных аккаунта, проверьте данные', category='error')
        status_code = 400
    finally:
        return status_code 
        