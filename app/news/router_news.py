"""
Модуль обработки запросов на получение новостей
Основные функции для обработки url + их описание:
news_page - Получение главной страницы с новостями
pages_scrolling(page_num) - Получение определенной страницы новостей
get_image_by_news_id(news_id) - Получение определенной фотографии по её айди,
    если такой фотографии в базе нет, берется фотография по умолчанию
add_news_page - Форма (и её обработка) для добавления новости в общую ленту
view_news_page(number_news) - Получение страницы конкретной новости по её айди 

"""
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
    user_id = current_user.get_id()
    return render_template(
        'news_page.html', 
        title='Новостная страница', 
        news_data_list=news_list, 
        current_page=1,
        user_id_viewer=user_id
        )


@news_router.route('/page/<int:page_num>')
def pages_scrolling(page_num: int):
    """Функция для отображения конкретной страницы новостей"""
    if page_num > 0:
        new_orm = NewsOrm()
        news_list: list[dict, dict] = new_orm.get_news_by_page_news(page_num=page_num)
        return render_template(
            'news_page.html', title='Новостная страница', 
            news_data_list=news_list, current_page=page_num
            )
    flash('Невозможно найти страницу с отрицательным индексом', category='error_news')
    return redirect(url_for('.news_page'))



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
        try:
            new_orm = NewsOrm()
            image_orm = ImageOrm()
            anons = request.form['anons']
            title = request.form['title']
            text = request.form['text']
            photo = request.files['photo']
            user_id = current_user.get_id()
            if not user_id:
                flash('Войдите в свой аккаунт для добавления новости', category='error')
                return redirect('/auth/login')
            img = None
            if photo:
                img = photo.read()
            news_id_in_db = new_orm.add_news_orm(anons=anons, title=title, text=text, author_id=user_id)
            image_orm.add_new_photo_news(img=img, f_id_new=news_id_in_db)
            flash('Добавление статьи прошло успешно', category='success_news')
            return redirect(url_for('.news_page'))
        except Exception as Error:
            flash('Ошибка добавления статьи в базу, проверьте корректность текста.',
                category='error')

    return render_template('add_news_page.html', title='Добавление статьи')

@news_router.route('/view_news/<int:number_news>')
@login_required
def view_news_page(number_news:int):
    """Обработчик для получения конкретной новости по её айди"""
    new_orm = NewsOrm()
    # Добавление 1 просмотра новости
    new_orm.add_news_view(news_id=number_news)
    news_info_from_db =  new_orm.get_info_by_id_new(news_id=number_news)
    if news_info_from_db:
        news_info = news_info_from_db[0]
        return render_template('news_number_page.html', title=f'Новость {news_info['id']}', data_news=news_info)
    
    return f"Новости с таким id нет"