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