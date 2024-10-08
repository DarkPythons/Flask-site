"""
Модуль, который содержит основные функции конвертации и обращение к API
get_json_response_from_currency_api: функция для обращение к API конвертора
confirm_data_by_response: преобразование ответа json формата в нормальный dict
creating_response_currency: 
"""
from flask import request, flash
import requests

from config import SettingByAPICurrency
from base_log import log_except, log_app

setting_currency = SettingByAPICurrency()

def get_json_response_from_currency_api(*, 
    from_currency_name: str, to_currency_name: str, amount: int
) -> dict:
    """
    Метод для обращения к API по конвертации валюты, возвращает json ответ.
    from_currency_name: из какой валюты делается преобразование
    to_currency_name: в какую валюту делается преобразование
    amount: количество валюты, которую нужно преобразовать
    """

    api_key = setting_currency.KEY_CURRENCY_API
    url = (f'https://api.getgeoapi.com/v2/currency/convert?api_key={api_key}'
    f'&from{from_currency_name}'
    f'&to={to_currency_name}'
    f'&amount={amount}'
    f'&format=json'
    )
    response = requests.get(url, headers=setting_currency.HEADERS_BY_REQ)
    response_json = response.json()
    return response_json

def confirm_data_by_response(*, response_json, form_to_currency_code) -> dict:
    """
    Метод, который на основе полученных данных из API, формирует dict,
    для отправки на фронтенд ответа пользователю.
    response_json: ответ от API конвертировщика
    form_to_currency_code: код валюты в которую нужно сделать конвертацию
    """
    #r - означает приставку response
    r_from_currency_code = response_json['base_currency_code']
    r_from_currency_name = response_json['base_currency_name']
    r_amount = response_json['amount']
    r_amount_round = round(float(r_amount), 2)
    r_last_update_date = response_json['updated_date']
    r_to_currency_name = response_json['rates'][form_to_currency_code]['currency_name']
    r_result_convert = response_json['rates'][form_to_currency_code]['rate_for_amount']
    r_result_convert_round = round(float(r_result_convert), 2)  
    data = {
        'result_convert' : r_result_convert_round,
        'amount' : r_amount_round,
        'from_currency_code' : r_from_currency_code,
        'from_currency_name' : r_from_currency_name,
        'to_currency_code' : form_to_currency_code,
        'to_currency_name' :  r_to_currency_name,
        'last_update_date' : r_last_update_date
    }
    return data


def creating_response_currency() -> dict:
    """
    Функция для создания конечного ответа пользователю, 
    данные которого будут отображаться на фронтендe.
    объединяет в себе функцию которая делает запрос к API,
    и функцию, которая формирует dict на основе полученного json от API 
    """
    status_code = 200
    try:
        #Получение данных из формы
        form_from_currency_name = request.form['from_currency']
        form_to_currency_code = request.form['to_currency']
        form_amount = request.form['amount']

        response_json = get_json_response_from_currency_api(
            from_currency_name=form_from_currency_name, 
            to_currency_name=form_to_currency_code, 
            amount=form_amount
            )
        full_data_dict = confirm_data_by_response(
            response_json=response_json,
            form_to_currency_code=form_to_currency_code
            )   
    except KeyError as Error:
        flash('Введены не все данные для выполнения запрооса.', category='error')
        log_except.error(f'Введены не все данные для выполнения запроса ковертирования: {Error}')
    except requests.JSONDecodeError as Error:
        flash('Ошибка сервера, обратитесь к этой функции чуть позже.', category='error')
        log_except.critical(f'Серсер не смог преобразовать ответ в json: {Error}')
    except (TypeError, ValueError) as Error:
        flash('Возникла ошибка при конвертации полученных данных от сервера.', category='error')
        log_except.critical(f'API конвертировщика выдало неправильные данные: {Error}')
    except Exception as Error:
        flash('Ошибка сервера', category='error')
        log_except.critical(f"Неопознаная ошибка при конвертировании: {Error}")
    else:
        log_app.info('Данные из API конвертировщика успешно получены')
        return {'status_code' : status_code, 'full_data_dict' : full_data_dict}
    status_code = 500
    return {'status_code' : status_code}