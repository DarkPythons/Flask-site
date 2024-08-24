from flask import Blueprint, request, render_template, flash
from config import SettingByAPICurrency
import requests

setting_currency = SettingByAPICurrency()

converter_router = Blueprint('converter_router', __name__,
    static_folder='static', 
    template_folder='templates')

@converter_router.route('/', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        flash('Конвертация прошла успешно', category='success')
        api_key = setting_currency.KEY_CURRENCY_API
        form_from_currency_name = request.form['from_currency']
        form_to_currency_code = request.form['to_currency']
        form_amount = request.form['amount']
        url = f'https://api.getgeoapi.com/v2/currency/convert?api_key={api_key}&from={form_from_currency_name}&to={form_to_currency_code}&amount={form_amount}&format=json'
        response = requests.get(url, headers=setting_currency.HEADERS_BY_REQ)
        response_json = response.json()
        response_from_currency_code = response_json['base_currency_code']
        response_from_currency_name = response_json['base_currency_name']
        response_amount = response_json['amount']
        response_amount_round = round(float(response_amount), 2)
        last_update_date = response_json['updated_date']

        response_to_currency_name = response_json['rates'][form_to_currency_code]['currency_name']
        response_result_convert = response_json['rates'][form_to_currency_code]['rate_for_amount']
        response_result_convert_round = round(float(response_result_convert), 2)


        return render_template('converter/converter_page.html', title='Конвертер валюты', result_convert=response_result_convert_round, amount=response_amount_round, from_currency_code=response_from_currency_code, from_currency_name=response_from_currency_name, to_currency_code=form_to_currency_code, to_currency_name=response_to_currency_name, last_update_date=last_update_date)

    return render_template('converter/converter_page.html', title='Конвертер валюты')

