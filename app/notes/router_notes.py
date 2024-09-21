from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from .notes_orm import NotesOrm

notes_router = Blueprint('notes_router', __name__, static_folder='static', template_folder='templates/notes')

@notes_router.route('/')
@login_required
def pages_notes():
    note_orm = NotesOrm()
    COUNT_RETURNS_NOTES = 15
    user_id = current_user.get_id()
    if user_id:
        notes_list = note_orm.get_notes_by_limit(limit_notes=COUNT_RETURNS_NOTES, author_id=user_id)
        return render_template('notes_page.html', title='Заметки', notes_data_list=notes_list)
    else:
        return redirect('/auth/login/')

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


@notes_router.route('/add_note', methods = ['POST', 'GET'])
@login_required
def add_note_page():
    if request.method == 'POST':
        note_orm = NotesOrm()
        status_code = add_new_notes_function(note_orm)
        if status_code == 200:
            flash('Добавление заметки прошло успешно', category='success_notes')
            return redirect('/notes/')
        else:
            flash('Проверьте корректность данных заметки, запись не удалась',
                category='error_notes')

    return render_template('notes_add.html', title='Добавление заметки')

@notes_router.route('/delete_note/<int:id_note>')
@login_required
def delete_note_page(id_note: int):
    note_orm = NotesOrm()
    user_id: int = current_user.get_id()
    status_author: bool = note_orm.check_note_and_author(id_note, user_id)
    if status_author:
        note_orm.delete_note_from_db(id_note)
        flash('Заметка была успешно удалена', category="success_notes")
    else:
        flash('Вы не являетесь автором этой заметки', category='error_notes')
    return redirect('/notes/')

@notes_router.route('/update_note/<int:id_note>', methods=['POST', 'GET'])
@login_required
def update_note_page(id_note: int):
    note_orm = NotesOrm()
    user_id: int = current_user.get_id()
    status_author: bool = note_orm.check_note_and_author(id_note, user_id)
    if status_author:
        if request.method == 'POST':
            new_name = request.form['name_notes']
            new_text = request.form['text_notes']
            note_orm.update_info_note(new_name=new_name, new_text=new_text, id_note=id_note)
            flash('Изменения были применены', category='success_notes')
            return redirect('/notes/')
        note_info = note_orm.get_note_info_by_id(id_note)
        return render_template('edit_note.html', title='Обновление заметки', note_data=note_info)
    else:
        flash('Вы не являетесь автором этой заметки', category='error_notes')
        return redirect('/notes/')

@notes_router.route('/view_note/<int:id_note>')
@login_required
def page_one_note(id_note: int):
    note_orm = NotesOrm()
    user_id: int = current_user.get_id()
    status_author: bool = note_orm.check_note_and_author(id_note, user_id)
    if status_author:
        note_info = note_orm.get_note_info_by_id(id_note)
        return render_template('one_note_page.html', title='Заметка', note_data= note_info)
    else:
        flash('Вы не являетесь автором этой заметки', category='error_notes')
        return redirect('/notes/')