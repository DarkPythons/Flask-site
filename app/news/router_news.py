from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from .news_orm import NewsOrm

news_router = Blueprint('news_router', __name__,
    static_folder='static',
    template_folder='templates/news'                    
    )



@news_router.route('/')
def news_page():
    new_orm = NewsOrm()
    news_list: list[dict, dict] = new_orm.get_first_news_orm()
    return render_template('news_page.html', title='Новостная страница', news_data_list=news_list)

@news_router.route('/add_news', methods=['POST', 'GET'])
@login_required
def add_news_page():
    if request.method == 'POST':
        new_orm = NewsOrm()
        anons = request.form['anons']
        title = request.form['title']
        text = request.form['text']
        photo = request.files.get('photo')
        user_id = current_user.get_id()
        img = None
        if photo:
            img = photo.read()

        new_orm.add_news_orm(anons=anons, title=title, text=text, author_id=user_id, img=img)
        return redirect(url_for('.news_page'))

    return render_template('add_news_page.html', title='Добавление статьи')

@news_router.route('/view_news/<int:number_page>')
@login_required
def view_news_page(number_page):
    return f"Страница номер {number_page}"