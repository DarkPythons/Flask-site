from flask import Blueprint, render_template, request, redirect, url_for, make_response,flash
from flask_login import login_required, current_user

from .news_orm import NewsOrm, ImageOrm

news_router = Blueprint('news_router', __name__,
    static_folder='static',
    template_folder='templates/news'                    
    )

@news_router.route('/')
def news_page():
    """Функция для отображения первой новостной страницы"""
    new_orm = NewsOrm()
    news_list: list[dict, dict] = new_orm.get_first_news_orm()
    return render_template('news_page.html', title='Новостная страница', news_data_list=news_list)


@news_router.route('/page/<int:page_num>')
def pages_scrolling(page_num: int):
    """Функция для отображения конкретной страницы новостей"""
    pass


@news_router.route('/image_news/<int:news_id>')
@login_required
def get_image_by_news_id(news_id: int):
    image_orm = ImageOrm()
    photo = image_orm.get_photo_from_db(f_id_new=news_id)
    if not photo:
        with open('static/image/photo_index.png', 'rb') as photo_file:
            photo = photo_file.read()
    response = make_response(photo)
    response.headers['Content-Type'] = 'image/jpg'
    return response


@news_router.route('/add_news', methods=['POST', 'GET'])
@login_required
def add_news_page():
    if request.method == 'POST':
        new_orm = NewsOrm()
        image_orm = ImageOrm()
        anons = request.form['anons']
        title = request.form['title']
        text = request.form['text']
        photo = request.files['photo']
        user_id = current_user.get_id()
        img = None
        if photo:
            img = photo.read()
        news_id_in_db = new_orm.add_news_orm(anons=anons, title=title, text=text, author_id=user_id)
        image_orm.add_new_photo_news(img=img, f_id_new=news_id_in_db)
        flash('Добавление статьи прошло успешно', category='success_news')
        return redirect(url_for('.news_page'))

    return render_template('add_news_page.html', title='Добавление статьи')

@news_router.route('/view_news/<int:number_news>')
@login_required
def view_news_page(number_news:int):
    new_orm = NewsOrm()
    new_orm.add_news_view(news_id=number_news)
    return f"Страница номер {number_news}"