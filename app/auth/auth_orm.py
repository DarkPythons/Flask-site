from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select

def loading_import_no_circule():
    from database import Users, db
    return {'users_db' : Users, "db_conn" : db}

class OrmRequest:
    
    def __init__(self):
        dict_param = loading_import_no_circule()
        self.db = dict_param['db_conn']
        self.session = self.db.session
        self.Users_model = dict_param['users_db']

    def register_user(self, username, email, psw):
        #Генерация пароля на основе алгоритма хеширования scrypt
        hashing_psw = generate_password_hash(psw)
        user = self.Users_model(username=username, email=email, psw=hashing_psw)
        self.session.add(user)
        self.session.flush()
        self.session.commit()

    def get_user_by_email(self, email_user):
        query = select(self.Users_model).where(self.Users_model.email == email_user).limit(1)
        result = self.session.execute(query)
        return result.first()
    
    def validate_password_user(self, user_obj, password_form):
        password_user_from_db = user_obj.psw
        result = check_password_hash(password_user_from_db, password_form)
        return result


    def get_rollback(self):
        self.session.rollback()
