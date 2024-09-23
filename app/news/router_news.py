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
from .utils import (update_data_news_function, get_authencticate_user, 
    add_news_function, add_photo_function)
from base_log import log_app, log_except

news_router = Blueprint('news_router', __name__,
    static_folder='static',
    template_folder='templates/news'                    
    )

@news_router.route('/')
def news_page():
    """Функция для отображения первой новостной страницы"""
    new_orm = NewsOrm()
    news_list: list[dict, dict] = new_orm.get_first_news_orm()
    user_id: str = current_user.get_id()
    if user_id:
        user_id: int = int(user_id)
    log_app.info(f'Пользователь с id {user_id} запросил страницу с новостями')
    return render_template(
        'news_page.html', 
        title='Новостная страница', 
        news_data_list=news_list, 
        current_page=1,
        user_id_viewer=user_id
        )

@news_router.route('/page/<int:page_num>')
def pages_scrolling(page_num: int):
    """
    Функция для отображения конкретной страницы новостей
    page_num: номер страницы новостей, которую запросил пользователь
    """
    if page_num > 0:
        new_orm = NewsOrm()
        news_list: list[dict, dict] = new_orm.get_news_by_page_news(page_num=page_num)
        return render_template(
            'news_page.html', title='Новостная страница', 
            news_data_list=news_list, current_page=page_num
            )
    flash('Невозможно найти страницу с отрицательным индексом', category='error_news')
    return redirect(url_for('.news_page'))

@news_router.route('/edit_news/<int:news_num>', methods=['POST', 'GET'])
@login_required
def edit_new_by_num(news_num: int):
    """
    Функция для изменения новости, при GET запросе возвращает форму для обновления данных,
    при POST запросе обрабатывает форму и обновляет данные новости
    news_num: id новости, которую пользователь хочет изменить
    """
    user_id = get_authencticate_user()
    new_orm = NewsOrm()
    news_info_from_db =  new_orm.get_info_by_id_new(news_id=news_num)
    if news_info_from_db:
        data_news = news_info_from_db[0]     
        # Если человек и вправду являеется создателем новости
        if data_news['author_id'] == user_id:
            if request.method == 'POST':
                status_update = update_data_news_function(new_orm=new_orm, news_num=news_num)
                if status_update == 200:
                    log_app.info(f'Новость с id {data_news["id"]} была изменена')
                    return redirect('/news') 
            return render_template('news_edit.html', title='Редактирование новости', 
                data_news=data_news)
        else:
            log_app.info(f'Пользователь {user_id} запросил изменение чужой новости')
            flash('Вы не можете редактировать чужие новости', category='error_news')
            return redirect('/news')

@news_router.route('/image_news/<int:news_id>')
def get_image_by_news_id(news_id: int):
    """Функция для получения картинки для новости, по id самой новости, так как
    в таблице фотографий, каждая фотография при помощи внешнего ключа связана со своей новостью
    news_id: id новости, при помощи которой будет получена нужная фотография
    """
    image_orm = ImageOrm()
    try:
        photo = image_orm.get_photo_from_db(f_id_new=news_id)
        if not photo:
            # Фотография по умолчанию
            with open('static/image/photo_index.png', 'rb') as photo_file:
                photo = photo_file.read()
        response = make_response(photo)
        response.headers['Content-Type'] = 'image/jpg'
        return response
    except (FileNotFoundError, Exception) as Error:
        log_except.critical(f'Ошибка получения фотографии по умолчанию {Error}')
        return 'Ошибка получения фотографии'

@news_router.route('/add_news', methods=['POST', 'GET'])
@login_required
def add_news_page():
    """Функция для отправки и обработки формы на добавление новости"""
    if request.method == 'POST':
        try:
            new_orm = NewsOrm()
            image_orm = ImageOrm()
            news_id_in_db = add_news_function(new_orm)
            add_photo_function(image_orm, news_id_in_db)
            flash('Добавление статьи прошло успешно', category='success_news')
            log_app.info(f'Новость была добавлена, её id {news_id_in_db}')
            return redirect(url_for('.news_page'))
        except Exception as Error:
            log_except.error(f'Ошибка добавления новости в базу: {Error}')
            flash('Ошибка добавления новости в базу, проверьте корректность текста.',
                category='error')
    return render_template('add_news_page.html', title='Добавление новости')

@news_router.route('/view_news/<int:number_news>')
@login_required
def view_news_page(number_news:int):
    """
    Обработчик для получения конкретной страницы с новостью
    number_news: id новости, которую запросил пользователь
    """
    new_orm = NewsOrm()
    # Добавление 1 просмотра к новости
    new_orm.add_news_view(news_id=number_news)
    news_info_from_db = new_orm.get_info_by_id_new(news_id=number_news)
    if news_info_from_db:
        news_info = news_info_from_db[0]
        log_app.info(f'Получена страница новости {news_info["id"]}')
        return render_template('news_number_page.html', 
            title=f'Новость {news_info['id']}', data_news=news_info)
    return render_template('not_found_news.html', title='Новость не найдена')