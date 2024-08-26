from sqlalchemy import select, update, delete

class NewsOrm:
    def __init__(self):
        from database import News, db
        self.db = db
        self.session = db.session
        self.News: News = News

    def get_first_news_orm(self):
        query = select(self.News.id, self.News.title, self.News.text, self.News.views, self.News.photo, self.News.author_id, self.News.anons).limit(10)
        result = self.session.execute(query)
        return result.mappings().all()

    def add_news_orm(self, *, anons, title, text, img, author_id):
        news = self.News(anons=anons, title=title, text=text, photo=img, author_id=author_id)
        self.session.add(news)
        self.session.commit()