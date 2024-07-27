from flask import Flask

from config import BaseSettingsApp
from router_main import router_main

app_settings = BaseSettingsApp()


app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(router_main, url_prefix="/")


if __name__ == "__main__":
    from database import create_table, drop_table
    create_table()
    app.run(debug=app_settings.PROJECT_ON_DEBUG)
    drop_table()
    