"""
Модуль, в котором лежат большие функции для сложных действий
add_new_notes_function: функция для добавления новой заметки, на основании данных из формы
update_note_function: функция для обновления данных заметки, на основании данных из формы
check_author: функция для проверки, является ли пользователь автором конкретной заметки 
    (определение может ли пользователь взаимодействовать с ней)
delete_note_function: функция для удаления конкретной заметки

"""
from flask import request, flash
from flask_login import current_user

from .notes_orm import NotesOrm

def add_new_notes_function(note_orm: NotesOrm):
    """
    Добавление новой заметки в таблицу
    note_orm: объект, который позволяет общаться с таблицей заметок
    """
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
    """
    Обновление данных о заметке (название, текст)
    note_orm: объект, который позволяет общаться с таблицей заметок
    id_note: id заметки, которую нужно обновить
    """
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
    """
    Функция для проверки является ли пользователь автором конкретной заметки
    note_orm: объект, который позволяет общаться с таблицей заметок
    id_note: id заметки, автора которой нужно проверить
    """
    user_id: int = current_user.get_id()
    status_author = True
    status_author: bool = note_orm.check_note_and_author(id_note, user_id)
    if status_author:
        return status_author
    else:
        flash('Вы не являетесь автором этой заметки', category='error_notes')

def delete_note_function(note_orm: NotesOrm, id_note: int):
    """
    Функция для удаления заметки из таблицы с заметками
    note_orm: объект, который позволяет общаться с таблицей заметок
    id_note: id заметки, которую нужно удалить из таблицы 
    """
    try:
        note_orm.delete_note_from_db(id_note)
        flash('Заметка была успешно удалена', category="success_notes")    
    except Exception as Error: 
        flash('Ошибка при удалении заметки')
