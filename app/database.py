import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, ForeignKey, BINARY
from flask_sqlalchemy import SQLAlchemy

from main import app

db = SQLAlchemy(app)


class Users(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    psw: Mapped[str] = mapped_column(db.String(500), nullable=False)
    date: Mapped[str] = mapped_column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<users {self.id}>"

class News(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    anons : Mapped[str] = mapped_column(db.String(50), nullable=False)
    title : Mapped[str] = mapped_column(db.String(100), nullable=False)
    text : Mapped[str] = mapped_column(db.String(15000), nullable=False)
    views : Mapped[int] = mapped_column(db.Integer, nullable=False, default=0)
    photo : Mapped[bin] = mapped_column(db.LargeBinary, nullable=True)

    author_id : Mapped[int] = mapped_column(ForeignKey(Users.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
 
    def __repr__(self):
        return f"<new {self.id}>"

class UserOrm:
    def __init__(self, db):
        self.db = db
    def get_user_by_id(self, user_id):
        result = db.session.query(Users).get(user_id)
        return result
        
def get_user_by_id(user_id):
    query = select(Users.id, Users.username, Users.email, Users.psw, Users.date).where(Users.id == user_id)
    result = db.session.execute(query)
    if result:
        list_result: list = result.mappings().all()
        if list_result:
            return list_result[0]
    return False



