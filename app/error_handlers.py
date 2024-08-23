"""Модуль для обработки распространенных ошибок"""
from flask import Blueprint, render_template

error_router = Blueprint('error_handlers', 
    __name__, 
    static_folder='static', 
    template_folder='templates/template_error')

@error_router.app_errorhandler(401)
def handler401(error):
    """
    Обработчик ошибки 401 
    (когда пользователь запросил ресурс, доступный только пользователям в аккаунте)
    """
    return (render_template('page401.html', title='Ошибка 401'), 401)

@error_router.app_errorhandler(403)
def handler403(error):
    """
    Обработчик ошибки 403 
    (когда пользователь запросил ресурс, доступный только авторизованным пользователям)
    """
    return (render_template('page403.html', title='Ошибка 403'), 403)

@error_router.app_errorhandler(404)
def handler404(error):
    """Обработчик ошибки 404 (когда пользователь перешёл на url, которого нет на сайте)"""
    return (render_template('page404.html', title='Ошибка 404'), 404)

@error_router.app_errorhandler(405)
def handler405(error):
    """Обработчик ошибки 405 (пользователь отправил метод запроса, который не поддерживается url)"""
    return (render_template('page405.html', title='Ошибка 405'), 405)

@error_router.app_errorhandler(500)
def handler500(error):
    """
    Обработчик ошибки 500 
    (на сервера произошла ошибка, поэтому пользователь не получил свой ресурс)
    """
    return (render_template('page500.html', title='Ошибка 500'), 500)

text_503 = """На сервере идёт техническое обслуживание, попробуйте вашу попытку чуть позже..."""

@error_router.app_errorhandler(503)
def handler503(error):
    """
    Обработчик ошибки 503 
    (сервер не готов дать ответ в данный момент времени (перегрузка, обновление сайта))
    """
    return (render_template('page503.html', title='Ошибка 503', text=text_503), 503)