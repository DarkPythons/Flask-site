"""
Модуль, в котором находятся все запросы к таблице с заметками в базе данных, через orm
NotesOrm: класс, в котором прописаны основные функции для обращения к таблице.
"""

from sqlalchemy import select, update, delete, insert

class NotesOrm:
    """Содержит основные функции для взаимодействия с таблицей заметок в базе."""
    def __init__(self):
        """Инициализация переменных и объектов для взаимодействия с базой данных"""
        from database import Notes, db
        self.db = db
        self.session = db.session
        self.Notes = Notes
        # Количество заметок на одной странице
        self.ONE_PAGE_LIMIT_NOTES = 15

    def get_note_info_by_id(self, id_note):
        """
        Получение информации о конкретной заметке из таблицы заметок по её id
        id_note: id заметки, информацию о которой мы хотим получить.
        """
        query = select(
                self.Notes.id, self.Notes.name_notes, 
                self.Notes.text_notes, self.Notes.author_id
            ).where(self.Notes.id == id_note)
        result = self.session.execute(query)
        return result.mappings().one()
    
    def get_notes_by_limit(self, *, author_id: int) -> list[dict, dict]:
        """
        Получение ограниченного количества заметок для конкретного пользователя
        author_id: id автора чьи заметки нам нужно получить
        """
        query = select(
            self.Notes.id, self.Notes.name_notes, self.Notes.text_notes, 
            self.Notes.author_id).where(
                self.Notes.author_id == author_id
            ).limit(self.ONE_PAGE_LIMIT_NOTES).order_by(self.Notes.id.desc())
        result = self.session.execute(query)
        return result.mappings().all()

    def add_new_notes(self, *, name_notes: str, text_notes: str, author_id: int):
        """Добавление новой заметки в таблицу заметок
        name_notes: название заметки
        text_notes: текст заметки
        author_id: id кому будет принадлежать заметка 
            (внешний ключ на таблицу с пользователями)
        """
        query = insert(self.Notes).values(
            name_notes=name_notes, text_notes=text_notes, author_id=author_id
        )
        self.session.execute(query)
        self.session.commit()

    def delete_note_from_db(self, id_note: int):
        """
        Удаление конкретной заметки из таблицы с заметками
        id_note: id заметки, которую нужно удалить
        """
        query = delete(self.Notes).where(self.Notes.id == id_note)
        self.session.execute(query)
        self.session.commit()

    def check_note_and_author(self, id_note: int, user_id: int) -> bool:
        """
        Функция для проверки, является ли заметка с определенным id пользователя который сделал
        запрос на её обновление/удаление/просмотр.
        id_note: aйди заметки.
        user_id: айди пользователя.
        """
        query = select(self.Notes.id).where(
            (self.Notes.id == id_note) & (self.Notes.author_id == user_id)
        )
        result = self.session.execute(query)
        if result:
            if result.all():
                return True
        return False
    
    def update_info_note(self, new_name: str, new_text: str, id_note: int):
        """Обновление информации о заметки из таблицы заметок
        new_name: новое имя для заметки
        new_text: новый текст для заметки
        id_note: id заметки, данные которой нужно обновить
        """
        query = update(self.Notes).values(
            name_notes=new_name, text_notes=new_text
        ).where(self.Notes.id == id_note)
        self.session.execute(query)
        self.session.commit()

    def get_notes_by_page(self, *, author_id: int, page_id: int) -> list:
        """
        Получение заметок пользователя на конкретной странице
        author_id: id автора чьи заметки нужно получить
        page_id: id страницы, на которую нужны заметки
        """
        # Высчитываем сколько записей мы должны пропустить
        offset_param = (page_id-1) * self.ONE_PAGE_LIMIT_NOTES
        query = select(
            self.Notes.id, self.Notes.name_notes, 
            self.Notes.text_notes, self.Notes.author_id
        ).where(
            self.Notes.author_id == author_id
            ).offset(offset_param).limit(self.ONE_PAGE_LIMIT_NOTES).order_by(self.Notes.id.desc())
        result = self.session.execute(query)
        return result.mappings().all()