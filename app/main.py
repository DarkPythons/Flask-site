from flask import Flask
from flask_login import LoginManager

from config import BaseSettingsApp, BaseSettingsDataBase
from router_main import main_router
from auth.router_auth import router_auth

db_setting = BaseSettingsDataBase()
from auth.auth_orm import OrmRequest

app_settings = BaseSettingsApp()


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = app_settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = db_setting.get_db_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Подключение SQLalchemy с нашим приложением







app.register_blueprint(main_router, url_prefix="/")
app.register_blueprint(router_auth, url_prefix='/auth')

if __name__ == "__main__":
    from database import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=app_settings.PROJECT_ON_DEBUG)
    with app.app_context():
        db.drop_all()
    