from sqlalchemy import select, update, delete, insert
from flask_sqlalchemy import SQLAlchemy


class NewsOrm:
    def __init__(self):
        from database import News, db
        self.db = db
        self.session = db.session
        self.News: News = News
        self.num_of_news_on_one_page = 15

    def get_first_news_orm(self):
        query = select(self.News.id, self.News.title, self.News.text, self.News.views, self.News.author_id, self.News.anons).order_by(self.News.id.desc()).limit(self.num_of_news_on_one_page)
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
    
    def add_news_view(self, *, news_id):
        query = update(self.News).values(views=(self.News.views+1)).where(self.News.id == news_id)
        self.session.execute(query)
        self.session.commit()

    def get_news_by_page_news(self, *, page_num: int):
        offset_param = (page_num-1) * self.num_of_news_on_one_page
        query = select(
            self.News.id, self.News.title, self.News.text, 
            self.News.views, self.News.author_id, self.News.anons
            # Делаем отсуп + ограничение количества новостей
            ).offset(offset_param).limit(self.num_of_news_on_one_page)
        result = self.session.execute(query)
        return result.mappings().all()
    
    def get_info_by_id_new(self, *, news_id: int):
        query = select(
            self.News.id, self.News.title, self.News.text,
            self.News.views, self.News.author_id, self.News.anons
        ).where(self.News.id == news_id)
        result = self.session.execute(query)
        return result.mappings().all()


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
        try:
            photo_from_orm = self.session.execute(photo_select_query)
            if photo_from_orm:
                return photo_from_orm.one()[0]
        except:
            return None

