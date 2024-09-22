from .notes_orm import NotesOrm
from flask import request, flash
from flask_login import current_user


def add_new_notes_function(note_orm: NotesOrm):
    status_code = 200
    try:
        name_notes = request.form['name_notes']
        text_notes = request.form['text_notes']
        author_id: int = current_user.get_id()
        note_orm.add_new_notes(name_notes=name_notes, text_notes=text_notes, author_id=author_id)
    except Exception as Error:
        status_code = 500
    finally:
        return status_code
def update_note_function(note_orm: NotesOrm, id_note: int):
    status = 200
    try:
        new_name = request.form['name_notes']
        new_text = request.form['text_notes']
        note_orm.update_info_note(new_name=new_name, new_text=new_text, id_note=id_note)
        flash('Изменения были применены', category='success_notes')
    except (KeyError, ValueError, TypeError) as Error:
        flash('Ошибка заполнения формы обновления заметки', category='error_notes')
        status = 400
    except Exception as Error:
        flash('Ошибка обновления заметки, проверьте заполненные поля на ошибки', category='error_notes')
        status = 500
    finally:
        return status
def check_author(note_orm: NotesOrm ,id_note: int):
    user_id: int = current_user.get_id()
    status_author = True
    status_author: bool = note_orm.check_note_and_author(id_note, user_id)
    if status_author:
        return status_author
    else:
        flash('Вы не являетесь автором этой заметки', category='error_notes')

def delete_note_function(note_orm: NotesOrm, id_note: int):
    try:
        note_orm.delete_note_from_db(id_note)
        flash('Заметка была успешно удалена', category="success_notes")    
    except Exception as Error: 
        flash('Ошибка при удалении заметки')
