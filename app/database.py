"""
Модуль, который содержит функции/классы для работы с базой данных через ORM
Users: класс для представления таблицы users в базе
News: класс для представления таблицы news в базе
Notes: класс для представления таблицы notes в базе
News_Image: класс для представления таблицы news_image в базе
get_user_by_id: функция для получения пользователя из базы по его id
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, ForeignKey
import datetime

from main import app

db = SQLAlchemy(app)

class Users(db.Model):
    """
    Представление таблицы users в базе данных,
    будет хранить данные о пользователях
    """
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    psw: Mapped[str] = mapped_column(db.String(500), nullable=False)
    date: Mapped[str] = mapped_column(db.DateTime, default=datetime.datetime.utcnow)
    about: Mapped[str] = mapped_column(db.String(1000), nullable=True)

    def __repr__(self):
        """Добавляем нормальное отображение объектов этого класса"""
        return f"<users {self.id}>"

class News(db.Model):
    """
    Представление таблицы news в базе данных,
    будет хранить данные новостей
    """
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    anons : Mapped[str] = mapped_column(db.String(50), nullable=False)
    title : Mapped[str] = mapped_column(db.String(100), nullable=False)
    text : Mapped[str] = mapped_column(db.String(15000), nullable=False)
    views : Mapped[int] = mapped_column(db.Integer, nullable=False, default=0)
    
    author_id : Mapped[int] = mapped_column(
        ForeignKey(Users.id, ondelete='RESTRICT', onupdate='CASCADE'), nullable=True
    )
 
    def __repr__(self):
        """Добавляем нормальное отображение объектов этого класса"""
        return f"<news {self.id}>"
    
class Notes(db.Model):
    """
    Представление таблицы notes в базе данных,
    будет хранить информацию о заметках пользователя
    """
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name_notes: Mapped[str] = mapped_column(db.String(50), nullable=False)
    text_notes: Mapped[str] = mapped_column(db.String(2000), nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey(Users.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    def __repr__(self):
        """Добавляем нормальное отображение объектов этого класса"""
        return f"<note {self.id}>"

class News_Image(db.Model):
    """
    Представление таблицы news_image в базе данныx,
    будет хранить фотографии, которые будут привязаны к новостям
    """
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    photo : Mapped[bin] = mapped_column(db.LargeBinary, nullable=True)
    f_id_new : Mapped[int] = mapped_column(
        ForeignKey(News.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=True
    )

    def __repr__(self):
        """Добавляем нормальное отображение объектов этого класса"""
        return f"<image {self.id}>"
  
def get_user_by_id(user_id: id):
    """
    Функция для получение информации о пользователе по его id, нужна в модуле UserLogin.py
    user_id: id пользователя, информацию о котором нужно получить
    """
    query = select(
        Users.id, Users.username, 
        Users.email, Users.psw, 
        Users.date
    ).where(Users.id == user_id)
    result = db.session.execute(query)
    if result:
        list_result: list = result.mappings().all()
        if list_result:
            return list_result[0]
    return False



