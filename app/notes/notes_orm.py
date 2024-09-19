from sqlalchemy import select, update, delete, insert

class NotesOrm:
    def __init__(self):
        from database import Notes, db
        self.db = db
        self.session = db.session
        self.Notes = Notes
    