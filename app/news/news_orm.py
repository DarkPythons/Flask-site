from sqlalchemy import select, update, delete

class NewsOrm:
    def __init__(self):
        from database import News, db
        self.db = db
        self.session = db.session
        self.News = News

    def get_ten_first_new(self):
        query = select(self.News.id, self.News.title, self.News.text, self.News.views, self.News.photo, self.News.author_id).limit(10)
        result = self.session.execute(query)
        return result.mappings().all()