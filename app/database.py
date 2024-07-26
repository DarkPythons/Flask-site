from config import BaseSettingsDataBase

db_setting = BaseSettingsDataBase()

DATABASE_URL = f"postgresql+psycopg2://\
{db_setting.DB_USER}:{db_setting.DB_PASS}@\
{db_setting.DB_HOST}:{db_setting.DB_PORT}/\
{db_setting.DB_NAME}"