from flask import Flask

from config import BaseSettingsApp
from router_main import router as main_router
from auth.router_auth import router as auth_router

app_settings = BaseSettingsApp()


app = Flask(__name__)
app.config.from_object(__name__)

app.register_blueprint(main_router, url_prefix="/")
app.register_blueprint(auth_router, url_prefix='/auth')

if __name__ == "__main__":
    from database import create_table, drop_table
    create_table()
    app.run(debug=app_settings.PROJECT_ON_DEBUG)
    drop_table()
    