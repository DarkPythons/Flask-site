"""
Модуль, который содержит основные классы для обращения к таблице новостей
и изображений
NewsOrm: класс, который содержит функции для работы с таблицей новостей
ImageOrm: класс, который содержит функции для работы с таблицей изображений 
"""

from sqlalchemy import select, update, delete, insert

class NewsOrm:
    """
    Содержит основные функции для обращения к таблице новостей в базе данных
    get_first_news_orm: получить список первых новостей для главной страницы
    add_news_orm: добавление новости в базу
    add_news_view: добавление просмотра конкретной новости
    get_news_by_page_news: получить список новостей на определенной странице
    get_info_by_id_new: получить информацию о новости по её id
    update_news_in_db: обновнить информацию новости
    """
    def __init__(self):
        """Инициализация объектов для работы с таблицей новостей"""
        from database import News, db
        self.db = db
        self.session = db.session
        self.News: News = News
        self.COUNT_NEWS_ONE_PAGE = 15

    def get_first_news_orm(self) -> list:
        """Получение списка новостей для первой (главной) страници"""
        query = select(
            self.News.id, self.News.title, 
            self.News.text, self.News.views, 
            self.News.author_id, self.News.anons
            ).order_by(self.News.id.desc()).limit(self.COUNT_NEWS_ONE_PAGE)
        result = self.session.execute(query)
        return result.mappings().all()

    def add_news_orm(self, *, anons: str, title: str, text: str, author_id: int) -> int:
        """
        Добавление новости в таблицу новостей.
        anons: заголовок новости
        title: название новости
        text: текст новости
        author_id: кто написал эту новость.
        Возвращает id добавленной новости
        """
        insert_new_query = insert(self.News).values(anons=anons, title=title, text=text, author_id=author_id).returning(self.News.id)
        returning_id = self.session.execute(insert_new_query)
        self.session.commit()
        result_id = returning_id.one()
        if result_id:
            return result_id[0]
        return result_id
    
    def add_news_view(self, *, news_id: int):
        """
        Добавление просмотра для определенной новости
        news_id: id новости, для которой делается прибавление просмотра
        """
        query = update(self.News).values(views=(self.News.views+1)).where(self.News.id == news_id)
        self.session.execute(query)
        self.session.commit()

    def get_news_by_page_news(self, *, page_num: int) -> list[dict, dict]:
        """
        Получение списка новостей для определенной страницы
        page_num: номер страницы новостей 
        """
        offset_param = (page_num-1) * self.COUNT_NEWS_ONE_PAGE
        query = select(
            self.News.id, self.News.title, self.News.text, 
            self.News.views, self.News.author_id, self.News.anons
            # Делаем отсуп + ограничение количества новостей
            ).order_by(self.News.id.desc()
            ).offset(offset_param).limit(self.COUNT_NEWS_ONE_PAGE)
        result = self.session.execute(query)
        return result.mappings().all()
    
    def get_info_by_id_new(self, *, news_id: int) -> dict:
        """
        Получение информации о конкретной новости по её id
        news_id: id новости, для которой нужно получить информацию
        """
        query = select(
            self.News.id, self.News.title, self.News.text,
            self.News.views, self.News.author_id, self.News.anons
        ).where(self.News.id == news_id)
        result = self.session.execute(query)
        return result.mappings().all()  
    
    def update_news_in_db(self, *, new_anons: str, new_title: str, 
        new_text: str, number_news: int):
        """
        Обновление информации конкретной новости
        new_anons: новый заголовок новости
        new_title: новое название для новости
        new_text: новый текст новости
        number_news: id новости, для которой нужно сделать изменение данных
        """
        query = update(self.News).values(
            anons=new_anons,
            title=new_title, 
            text=new_text
            ).where(self.News.id == number_news)
        self.session.execute(query)
        self.session.commit()


class ImageOrm:
    """
    Содержит основные функции для работы с таблицей изображений
    add_new_photo_news: Добавление фотографии, которая будет привязана к новости
    get_photo_from_db: Получить фотографию, которая привязана к какой-то новости
    update_photo_by_news_id: Обновление фотографии для новости
    """
    def __init__(self):
        """Инициализация объектов для работы с таблицей изображений"""
        from database import News_Image, db
        self.db = db
        self.session = db.session
        self.News_Image: News_Image = News_Image
    
    def add_new_photo_news(self, *, img: bin, f_id_new: int):
        """
        Добавление изображения в таблицу
        img: бинарный вид изображения, который будет сохранен в базу
        f_id_new: id новости, на которое будет ссылаться изображение
        """
        insert_new_photo = insert(self.News_Image).values(photo=img, f_id_new=f_id_new)
        self.session.execute(insert_new_photo)
        self.session.commit()

    def get_photo_from_db(self, *, f_id_new: int) -> bin:
        """
        Получение изображения из таблицы изображений в базе
        f_id_new: id новости, по которому будет происходить поиск изображения
        """
        photo_select_query = select(
            self.News_Image.photo
            ).where(self.News_Image.f_id_new == f_id_new)
        try:
            photo_from_orm = self.session.execute(photo_select_query)
            if photo_from_orm:
                return photo_from_orm.one()[0]
        except:
            return None

    def update_photo_by_news_id(self, *, new_img: bin, number_news: int):
        """
        Обновление изображения для новости
        new_img: бинарный вид нового изображения
        number_news: id новости, для которой будет обновлено изображение
        """
        query = update(self.News_Image).values(photo=new_img).where(
            self.News_Image.f_id_new == number_news
            )
        self.session.execute(query)
        self.session.commit()