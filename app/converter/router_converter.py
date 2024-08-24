from flask import Blueprint, request, render_template, flash
from config import SettingByAPICurrency
import requests

setting_currency = SettingByAPICurrency()

converter_router = Blueprint('converter_router', __name__,
    static_folder='static', 
    template_folder='templates')


def get_json_response_from_currency_api(*, from_currency_name, to_currency_name, amount) -> dict:
    api_key = setting_currency.KEY_CURRENCY_API
    url = f'https://api.getgeoapi.com/v2/currency/convert?api_key={api_key}&from{from_currency_name}&to={to_currency_name}&amount={amount}&format=json'
    response = requests.get(url, headers=setting_currency.HEADERS_BY_REQ)
    response_json = response.json()
    return response_json

def confirm_data_by_response(*, response_json, form_to_currency_code):
    """
    Метод, который на основе полученных данных из API, формирует dict,
    для отправки на фронтенд ответа пользователю.
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
    #Получение данных из формы
    form_from_currency_name = request.form['from_currency']
    form_to_currency_code = request.form['to_currency']
    form_amount = request.form['amount']

    response_json = get_json_response_from_currency_api(
        from_currency_name=form_from_currency_name, 
        to_currency_name=form_to_currency_code, 
        amount=form_amount
        )
    
    full_data_dict = confirm_data_by_response(response_json=response_json, form_to_currency_code=form_to_currency_code)

  
    return full_data_dict

@converter_router.route('/', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        flash('Конвертация прошла успешно', category='success')

        data: dict = creating_response_currency()
        

        return render_template('converter/converter_page.html', title='Конвертер валюты', **data)

    return render_template('converter/converter_page.html', title='Конвертер валюты')

