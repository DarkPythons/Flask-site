<p align="center">
      <img src="https://i.ibb.co/0XcwvjC/photo.jpg" alt="API Restorunt" border="0" width="727">
</p>

<p align="center">
   <img alt="Static Badge" src="https://img.shields.io/badge/Licencse-MIT-success">
   <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/Flask">
  <img alt="PyPI - Python Version" src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json">
</p>

## About

Этот сайт написан на Flask, при помощи Bootstrap у сайта есть красивый фронтенд, а при помощи Flask сильный бекенд. 
На сайте есть множество функций: конвертация валюты, написание/чтение/изменение новостей, заметок, свой профиль.

## Documentation

<h3>Базовая настройка</h3>
<ol>
<li>Скачайте проект с githun командой: git clone https://github.com/DarkPythons/Flask-site.git</li>
<li>Используя консоль перейдите к файлам проекта</li>
<li>Устновите зависимости из файла requirements при помощи команды: pip install -r requirements.txt</li>
<ul>
<li>Или при помощи файла pyproject.toml, находясь в консоли в том же каталоге что и pyproject.toml, введите: poetry install</li>
<li>После чего у вас появится виртуальная среда со всеми зависимостями, войдите в эту среду с помощью команды: poetry shell</li>
</ul>
<li>Создайте и настройте файл .env при использовании примера в виде файла .env_example</li>
</ol>

<h3>Запуск приложения</h3>
<ol>
<li>После настройки среды с зависимостями и файла .env вы можете запустить приложение</li>
<li>Перейдите в каталог /app через терминал и введите команду: python main.py</li>
      <ul>
            <li>Или запустите приложение через окружение poetry с помощью команды: poetry run python main.py</li>
      </ul>
<li>После этого сайт должен начать работу по url: http://127.0.0.1:5000/</li>
<li>Перейдите на этот url после полного запуска приложения, логирование включается вместе с запуском.</li>
</ol>

<h3>После открытия сайта по url http://127.0.0.1:5000/ вы должны увидеть следующее:</h3>
<img src="https://i.ibb.co/nLMrnXQ/index.png" alt="index page" border="0" width="300" height="500">


## Distribute

## Developers

- [DarkPythons](https://github.com/DarkPythons)

## License
The Flask-site project is distributed under the MIT license.

## Примеры страниц на запущенном сайте
<p>
      <img src="https://i.ibb.co/1Zj7WLV/notes.png" border="0" width="300" height="450">
      <img src="https://i.ibb.co/jgDKzPJ/weather.jpg" alt="weather" border="0" width="300" height="450">
      <img src="https://i.ibb.co/sF5CR0Z/notes.jpg" alt="notes" border="0" width="280" height="450">
</p>
