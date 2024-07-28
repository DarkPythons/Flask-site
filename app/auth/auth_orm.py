from werkzeug.security import generate_password_hash, check_password_hash

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
        hashing_psw = generate_password_hash(psw)
        user = self.Users_model(username=username, email=email, psw=hashing_psw)
        self.session.add(user)
        self.session.flush()
        self.session.commit()

    def get_rollback(self):
        self.session.rollback()
