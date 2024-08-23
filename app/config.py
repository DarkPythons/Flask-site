from pydantic_settings import BaseSettings, SettingsConfigDict  #type: ignore
from dotenv import load_dotenv, find_dotenv
from pydantic import Field

load_dotenv(find_dotenv())

class BaseConfigClassInFile(BaseSettings):
    """Родительский класс, где указываем настройки, как и откуда будем брать данные из окружения"""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        #Чувстительность к регистрку
        case_sensitive=True
    )

class BaseSettingsDataBase(BaseConfigClassInFile):
    """Указывем базовые настройки для подключения к базе данных (Postgresql)"""

    #Данные в default представлены в виде примера
    DB_USER:str = Field(min_length=1, max_length=30, default="postgres")
    DB_PASS:str = Field(min_length=5, max_length=100)
    DB_HOST:str = Field(min_length=1, max_length=15, default='127.0.0.1')
    DB_PORT:str = Field(min_length=1, max_length=10, default='5432')
    DB_NAME:str = Field(min_length=1, max_length=100, default='praktika_flask')

    def get_db_url(self):
        """Метод возвращает url для подключения к базе данных, по настройкам из окружения,
        данные из которого берутся выше"""
        return f"postgresql+psycopg2://\
{self.DB_USER}:{self.DB_PASS}@\
{self.DB_HOST}:{self.DB_PORT}/\
{self.DB_NAME}"

class BaseSettingsApp(BaseConfigClassInFile):
    """Класс для взятия данных из окружения, для настройки приложения в целом"""
    PROJECT_ON_DEBUG:bool = Field(default=True)
    SECRET_KEY:str = Field(min_length=5, max_length=50)

headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }

class SettingByAPICurrency(BaseConfigClassInFile):
    """Класс для взятия данных из окружения, для настройки API валюты"""
    KEY_CURRENCY_API:str = Field(min_length=3)
    HEADERS_BY_REQ:dict = Field(default=headers)