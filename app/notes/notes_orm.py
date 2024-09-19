from sqlalchemy import select, update, delete, insert

class NotesOrm:
    def __init__(self):
        from database import Notes, db
        self.db = db
        self.session = db.session
        self.Notes = Notes
    
    def add_new_notes(self, *, name_notes, text_notes, author_id):
        query = insert(self.Notes).values(name_notes=name_notes, text_notes=text_notes, author_id=author_id)
        self.session.execute(query)
        self.session.commit()

    def check_note_and_author(self, id_note, user_id) -> bool:
        query = select(self.Notes).where((self.Notes.id == id_note) & (self.Notes.author_id == user_id))
        result = self.session.execute(query)
        if result:
            if result.all():
                return True

        return False