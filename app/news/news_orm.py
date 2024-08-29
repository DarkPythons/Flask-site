from sqlalchemy import select, update, delete, insert
from flask_sqlalchemy import SQLAlchemy
import sqlite3

class NewsOrm:
    def __init__(self):
        from database import News, db
        self.db = db
        self.session = db.session
        self.News: News = News

    def get_first_news_orm(self):
        query = select(self.News.id, self.News.title, self.News.text, self.News.views, self.News.author_id, self.News.anons).limit(10)
        result = self.session.execute(query)
        return result.mappings().all()

    def add_news_orm(self, *, anons, title, text, author_id):
        insert_new_query = insert(self.News).values(anons=anons, title=title, text=text, author_id=author_id).returning(self.News.id)
        returning_id = self.session.execute(insert_new_query)
        self.session.commit()
        result_id = returning_id.one()
        if result_id:
            return result_id[0]
        return result_id
    
class ImageOrm:
    def __init__(self):
        from database import News_Image, db
        self.db = db
        self.session = db.session
        self.News_Image: News_Image = News_Image
    
    def add_new_photo_news(self, *, img, f_id_new):
        insert_new_photo = insert(self.News_Image).values(photo=img, f_id_new=f_id_new)
        self.session.execute(insert_new_photo)
        self.session.commit()

    def get_photo_from_db(self, *, f_id_new):
        photo_select_query = select(self.News_Image.photo).where(self.News_Image.f_id_new == f_id_new)
        photo_from_orm = self.session.execute(photo_select_query)
        if photo_from_orm:
            return photo_from_orm.one()[0]
        return None
