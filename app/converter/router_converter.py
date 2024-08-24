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
        from_valute = request.form['from_c']
        to_valut = request.form['to_c']
        amount = request.form['amount']
        url = f'https://api.getgeoapi.com/v2/currency/convert?api_key={api_key}&from={from_valute}&to={to_valut}&amount={amount}&format=json'
        response = requests.get(url, headers=setting_currency.HEADERS_BY_REQ)
        response_json = response.json()
        # Код введенной валюты от которой должна быть конвертация
        from_c_code = response_json['base_currency_code']
        # Имя введеной валюты
        from_c_name = response_json['base_currency_name']
        # Введенное количество валюты
        c_amount = response_json['amount']
        c_amount = round(float(c_amount), 2)
        # Последнее обновление данных
        update_date = response_json['updated_date']

        # Имя валюты, в которую нужно было конвертировать
        to_c_name = response_json['rates'][to_valut]['currency_name']
        # Стоимость одной единицы этой валюты
        c_rate = response_json['rates'][to_valut]['rate']
        # Результат (amount * c_rate)
        result = round(float(response_json['rates'][to_valut]['rate_for_amount']), 2)

        return render_template('converter/converter_page.html', title='Конвертер валюты', result=result, amount=c_amount, from_c_code=from_c_code, from_c_name=from_c_name, to_c_code=to_valut, to_c_name=to_c_name, time=update_date)

    return render_template('converter/converter_page.html', title='Конвертер валюты')

