"""
Модуль для обработки запросов на конвертирование валюты
converter: выдает и обрабатывает форму для конвертации валюты
"""
from flask import Blueprint, request, render_template, flash

from .utils import creating_response_currency

converter_router = Blueprint('converter_router', __name__,
    static_folder='static', 
    template_folder='templates/converter')

@converter_router.route('/', methods=['GET', 'POST'])
def converter():
    """
    При GET запросе отдает html форму, которую нужно заполнить, чтобы сделать конвертирование,
    после чего делается отправление данных этой формы через POST запрос, на основе данных формы,
    делается конвертирование и возвращается результат.
    """
    if request.method == 'POST':
        data: dict = creating_response_currency()
        if data['status_code'] == 200:
            flash('Конвертация прошла успешно', category='success')
            full_data_by_sending = data['full_data_dict']
            return render_template('converter_page.html', 
                title='Конвертер валюты', 
                **full_data_by_sending)
    return render_template('converter_page.html', title='Конвертер валюты')

