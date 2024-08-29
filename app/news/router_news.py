from flask import Blueprint, render_template, request, redirect, url_for, make_response
from flask_login import login_required, current_user

from .news_orm import NewsOrm, ImageOrm

news_router = Blueprint('news_router', __name__,
    static_folder='static',
    template_folder='templates/news'                    
    )



@news_router.route('/')
def news_page():
    new_orm = NewsOrm()
    news_list: list[dict, dict] = new_orm.get_first_news_orm()
    return render_template('news_page.html', title='Новостная страница', news_data_list=news_list)


@news_router.route('/image_news/<int:news_id>')
@login_required
def get_image_by_news_id(news_id: int):


    photo_orm = ImageOrm()
    photo_from_db = photo_orm.get_photo_from_db(f_id_new=news_id)
    response = make_response(photo_from_db)
    response.headers['Content-Type'] = 'image/jpg'
    return response


@news_router.route('/add_news', methods=['POST', 'GET'])
@login_required
def add_news_page():
    if request.method == 'POST':
        new_orm = NewsOrm()
        photo_orm = ImageOrm()
        anons = request.form['anons']
        title = request.form['title']
        text = request.form['text']
        photo = request.files['photo']
        user_id = current_user.get_id()
        img = None
        if photo:
            img = photo.read()
        news_id_in_db = new_orm.add_news_orm(anons=anons, title=title, text=text, author_id=user_id)
        photo_orm.add_new_photo_news(img=img, f_id_new=news_id_in_db)
        return redirect(url_for('.news_page'))

    return render_template('add_news_page.html', title='Добавление статьи')

@news_router.route('/view_news/<int:number_page>')
@login_required
def view_news_page(number_page):
    return f"Страница номер {number_page}"