"""
Модуль который содержит основную логику для работы с пользовательскими сессиями
UserLogin: содержит все нужные функции для работы с пользователем 
"""
from flask import redirect, url_for

class UserLogin():
    """Класс для работы с сессиями пользователей"""
    def fromDB(self, user_id: int):
        """Получение аккаунта пользователя из базы данных"""
        from database import get_user_by_id
        self.__user = get_user_by_id(user_id)
        return self
    
    def create(self, user):
        """
        Создание пользователя (сессии пользователя) на основе данных из базы
        user: объект пользователя со всеми его данными
        """
        self.__user = user
        return self

    def is_authenticated(self):
        """
        Проверка есть ли у пользователя сессия (если сессии не будет, эта функция не отработает)
        """
        return True
    def is_active(self):
        """
        Активен ли пользователь, если у него будет сессия, значит он активен
        """
        return True
    def is_anonymous(self):
        """
        Если у пользователя есть сессия, значит нам будет возвращен объект UserLogin,
        у которого и будет эта функция, а так как у него есть сессия, он не анонимен.
        """
        return False
    def get_id(self):
        """
        Получение айди пользователя из сессии, которая хранит данные базы
        """
        try:
            return str(self.__user['id'])
        except TypeError:
            return redirect(url_for('router_auth.logout'))
    #__user - хранит полученные данные из базы
    def get_name(self):
        """Получение имени из сессии (базы)"""
        return self.__user['username'] if self.__user else "Без имени"
    
    def get_email(self):
        """Получение mail-a из сессии (базы)"""
        return self.__user['email'] if self.__user else "Без email"
