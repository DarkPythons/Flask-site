from flask import redirect, url_for



class UserLogin():
       
    def fromDB(self, user_id):
        from database import get_user_by_id
        self.__user = get_user_by_id(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        try:
            return str(self.__user['id'])
        except TypeError:
            return redirect(url_for('router_auth.logout'))
    #__user - хранит полученные данные из базы
    def get_name(self):
        return self.__user['username'] if self.__user else "Без имени"
    
    def get_email(self):
        return self.__user['email'] if self.__user else "Без email"
