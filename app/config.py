import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv
from pydantic import Field

load_dotenv(find_dotenv())

class BaseConfigClassInFile(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        #Чувстительность к регистрку
        case_sensitive=True
    )

class BaseSettingsDataBase(BaseConfigClassInFile):
    #Данные в default представлены в виде примера
    DB_USER:str = Field(min_length=1, max_length=30, default="postgres")
    DB_PASS:str = Field(min_length=5, max_length=100)
    DB_HOST:str = Field(min_length=1, max_length=15, default='127.0.0.1')
    DB_PORT:str = Field(min_length=1, max_length=10, default='5432')
    DB_NAME:str = Field(min_length=1, max_length=100, default='praktika_flask')

    def get_db_url(self):
        return f"postgresql+psycopg2://\
{self.DB_USER}:{self.DB_PASS}@\
{self.DB_HOST}:{self.DB_PORT}/\
{self.DB_NAME}"

class BaseSettingsApp(BaseConfigClassInFile):
    PROJECT_ON_DEBUG:bool = Field(default=True)