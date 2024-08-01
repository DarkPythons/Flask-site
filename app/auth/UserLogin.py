from flask import url_for


class UserLogin():
    def fromDB(self, user_id):
        from database import get_user_by_id
        self.__user = get_user_by_id(user_id)
        return self
    def create(self, user):
        self.__user[0] = user
        return self

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.__user[0].id)

    #__user - хранит полученные данные из базы
    def getName(self):
        return self.__user[0]['name'] if self.__user else "Без имени"
    
    def getEmail(self):
        return self.__user[0]['email'] if self.__user else "Без email"
