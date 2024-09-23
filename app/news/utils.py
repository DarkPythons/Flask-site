"""
Модуль, в котором лежат большие или просто функции, которые нужно вынести из модуля, где обработчики
get_authencticate_user: получение id пользователя или просьба войти в аккаунт, 
    если получить id невозможно
update_data_news_function: функция для обновления данных новости

"""

from flask import flash, redirect, request 
from flask_login import current_user

from .news_orm import NewsOrm, ImageOrm

def get_authencticate_user():
    user_id = current_user.get_id()
    if user_id:
        user_id = int(user_id)
        return user_id
    else:
        flash('Войдите в аккаунт', category='error')
        return redirect('/auth/login')     

def update_data_news_function(new_orm: NewsOrm, news_num: int):
    """
    Функция для обновления данных новости (название, анонс, текст, фото),
    на новые данные из заполненной формы.
    new_orm: объект, позволяющий работать с таблицей новостей
    news_num: id новости, которую нужно обновить 
    """
    status_code = 200
    try:
        image_orm = ImageOrm()
        new_anons = request.form['anons']
        new_title = request.form['title']
        new_text = request.form['text']
        photo = request.files['photo']
        img = None
        if photo:
            img = photo.read()
        new_orm.update_news_in_db(
            new_anons=new_anons, 
            new_title=new_title, 
            new_text=new_text, 
            number_news=news_num)
        if img:
            image_orm.update_photo_by_news_id(new_img=img, number_news=news_num)
        flash('Изменение новости прошло успешно', category='success_news') 
    except (KeyError, ValueError, TypeError) as Error:
        flash('Ошибка при изменении новости, повторите позже', category='error_news')
        status_code = 500
    except Exception as Error:
        flash('Проверьте правильность введеных значений', category='error_news')
        status_code = 400
    finally:
        return status_code
    
def add_news_function(new_orm: NewsOrm):
    """
    Функция для добавления новости в базу
    new_orm: объект, позволяющий работать с таблицей новостей
    """
    anons = request.form['anons']
    title = request.form['title']
    text = request.form['text']
    user_id = current_user.get_id()
    news_id_in_db = new_orm.add_news_orm(anons=anons, title=title, text=text, author_id=user_id)
    return news_id_in_db

def add_photo_function(image_orm: ImageOrm, news_id_in_db):
    """
    Функция для добавления изображения, которое будет привязано к конкретной новости
    image_orm: объект, позволяющий работать с таблицей изображений
    news_id_in_db: id новости, к которому должна быть привязка добавляемой фотографии
    """
    photo = request.files['photo']
    img = None
    if photo:
        img = photo.read()
    image_orm.add_new_photo_news(img=img, f_id_new=news_id_in_db)   