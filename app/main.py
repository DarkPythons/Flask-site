from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from database import DATABASE_URL
from config import BaseSettingsApp

app_settings = BaseSettingsApp()


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Подключение SQLalchemy с нашим приложением
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=app_settings.PROJECT_ON_DEBUG)