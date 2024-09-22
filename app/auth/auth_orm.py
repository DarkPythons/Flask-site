"""
Модуль, который содержит orm для общения с таблицей пользователей в базе
AuthOrm: класс, который содержит основные функции для взаимодействия с таблицей пользователей 
"""
from sqlalchemy import select, update
from werkzeug.security import generate_password_hash, check_password_hash

class AuthOrm:
    """Содержит в себе основные функции для взаимодействия с таблицей пользователей"""
    def __init__(self):
        """Инициализация переменных и объектов для взаимодействия с базой данных"""
        from database import Users, db
        self.db = db
        self.session = db.session
        self.Users = Users

    def register_user(self, username: str, email: str, psw: str):
        """
        Регистрирование пользователя на основе данных, которые он ввёл в форме
        username: Имя пользователя
        email: mail пользователя
        psw: пароль пользователя (будет сохранен в виде хеша)
        """
        #Генерация пароля на основе алгоритма хеширования scrypt
        hashing_psw = generate_password_hash(psw)
        user = self.Users(username=username, email=email, psw=hashing_psw)
        self.session.add(user)
        self.session.commit()

    def get_user_by_email(self, email_user: str):
        """
        Получение данных о пользователе по его email
        email_user: mail пользователя, по которому мы будем искать пользователя
        """
        query = select(self.Users.id, 
            self.Users.email, 
            self.Users.date, 
            self.Users.username,
            self.Users.about,
            self.Users.psw).where(self.Users.email == email_user).limit(1)
        result = self.session.execute(query)
        if result:
            list_result:list = result.mappings().all()
            if list_result:
                return list_result[0]
        return False
        
    def validate_password_user(self, password_user, password_form):
        """
        Совпадает ли хеш пароля из таблицы, с хешом пароля, который ввел пользователь в форме входа
        password_user: хеш пароля из таблицы пользователей
        password_form: пароль из формы, который ввёл пользователь
        """
        password_user_from_db = password_user
        result = check_password_hash(password_user_from_db, password_form)
        return result

    def get_rollback(self):
        """
        Сделать откат изменений, которые были сделаны в транзакции
        """
        self.session.rollback()

    def update_data_user(self, *, new_username: str, new_about: str, user_id: int):
        """
        Обновление данных о пользователе, можно обновить имя пользователя и о себе
        new_username: новое имя для пользователя
        new_about: новое описание себя в профиле
        user_id: id пользователя, для которого нужно это обновление
        """
        query = update(self.Users).values(
            username=new_username, about=new_about
        ).where(self.Users.id == user_id)
        self.session.execute(query)
        self.session.commit()