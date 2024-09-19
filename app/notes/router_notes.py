from flask import Blueprint


notes_router = Blueprint('notes_router', __name__, static_folder='static', template_folder='templates/notes')

@notes_router.route('/')
def pages_notes():
    return "Главная страница заметок"
