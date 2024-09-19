from flask import Flask
from flask_login import LoginManager

from config import BaseSettingsApp, BaseSettingsDataBase
from router_main import main_router
from auth.router_auth import auth_router
from error_handlers import error_router
from converter.router_converter import converter_router
from news.router_news import news_router
from notes.router_notes import notes_router

db_setting = BaseSettingsDataBase()

app_settings = BaseSettingsApp()


app = Flask(__name__)



app.config.from_object(__name__)
app.config['SECRET_KEY'] = app_settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = db_setting.get_db_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



login_manager = LoginManager(app)
login_manager.view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    from auth.UserLogin import UserLogin
    return UserLogin().fromDB(user_id)

app.register_blueprint(main_router, url_prefix="/")
app.register_blueprint(auth_router, url_prefix='/auth')
app.register_blueprint(error_router)
app.register_blueprint(converter_router, url_prefix="/convert")
app.register_blueprint(news_router, url_prefix='/news')
app.register_blueprint(notes_router, url_prefix='/notes')

if __name__ == "__main__":
    from database import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=app_settings.PROJECT_ON_DEBUG)
    with app.app_context():
        db.drop_all()
    