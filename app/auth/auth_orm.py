from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select



class OrmRequest:
    
    def __init__(self):
        from database import Users, db
        self.db = db
        self.session = db.session
        self.Users = Users

    def register_user(self, username, email, psw):
        #Генерация пароля на основе алгоритма хеширования scrypt
        hashing_psw = generate_password_hash(psw)
        user = self.Users(username=username, email=email, psw=hashing_psw)
        self.session.add(user)
        self.session.commit()

    def get_user_by_email(self, email_user):
        query = select(self.Users.id, 
            self.Users.email, 
            self.Users.psw, 
            self.Users.date, 
            self.Users.username).where(self.Users.email == email_user).limit(1)
        result = self.session.execute(query)
        if result:
            list_result:list = result.mappings().all()
            if list_result:
                return list_result[0]
        return False
        
    def validate_password_user(self, password_user, password_form):
        password_user_from_db = password_user
        result = check_password_hash(password_user_from_db, password_form)
        return result


    def get_rollback(self):
        self.session.rollback()
