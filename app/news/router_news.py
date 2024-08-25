from flask import Blueprint, render_template, request
from flask_login import login_required

from .news_orm import NewsOrm

news_router = Blueprint('news_router', __name__,
    static_folder='static',
    template_folder='templates/news'                    
    )



@news_router.route('/')
def news_page():
    new_orm = NewsOrm()
    ten_news = new_orm.get_ten_first_new()
    return render_template('news_page.html', title='Новостная страница')

@news_router.route('/add_news', methods=['POST', 'GET'])
@login_required
def add_news_page():
    if request.method == 'POST':
        pass

    return render_template('add_news_page.html', title='Добавление статьи')