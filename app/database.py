import datetime
from sqlalchemy.orm import Mapped, mapped_column
from main import app
from flask_sqlalchemy import SQLAlchemy
from config import BaseSettingsDataBase




import datetime

db = SQLAlchemy(app)


class Users(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    psw: Mapped[str] = mapped_column(db.String(500), nullable=False)
    date: Mapped[str] = mapped_column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<users {self.id}>"



# def create_table():
#     with app.app_context():
#         db.create_all()
# def drop_table():
#     with app.app_context():
#         db.drop_all()



