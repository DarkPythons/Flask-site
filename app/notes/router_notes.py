"""
Модуль, в котором содержатся обработчики запросов на странице заметок,
доступны функции для удаления/изменения/просмотра заметок.
pages_notes: Получение первой (главной) страницы с новостями
pages_notes_pagination(page_id): Получение конкретной страницы (page_id) с заметками
page_one_note(id_note): Получение полной информации (название, описание) о заметке
add_note_page: Получение и обработка формы для добавления заметки
update_note_page(id_note): Получение и обработка формы для обновления заметки
delete_note_page(id_note): Удаление конкретной заметки по её айди в базе
"""

from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user

from .notes_orm import NotesOrm
from .utils import add_new_notes_function, check_author, update_note_function, delete_note_function

notes_router = Blueprint('notes_router', __name__,
    static_folder='static', template_folder='templates/notes')

@notes_router.route('/')
@login_required
def pages_notes():
    """Обработка запроса на получение главной страницы заметок"""
    note_orm = NotesOrm()
    user_id = current_user.get_id()
    if user_id:
        notes_list = note_orm.get_notes_by_limit(author_id=user_id)
        return render_template('notes_page.html', title='Заметки',
            notes_data_list=notes_list, page_id=1)
    else:
        return redirect('/auth/login')

@notes_router.route('/page/<int:page_id>')
@login_required
def pages_notes_pagination(page_id: int):
    """
    Обработка запроса на получение конкретной страницы заметок пользователя
    page_id: айди страницы которую запрашивает пользователь
    """
    note_orm = NotesOrm()
    user_id = current_user.get_id()
    if user_id:
        notes_list_data: list = note_orm.get_notes_by_page(author_id=user_id, page_id=page_id)
        return render_template(
            'notes_page.html', title=f'Заметки, страница {page_id}', 
            notes_data_list=notes_list_data, page_id=page_id
        )
    else:
        return redirect('/auth/login')

@notes_router.route('/view_note/<int:id_note>')
@login_required
def page_one_note(id_note: int):
    """
    Обработка запроса на получение конкретной заметки
    id_note: айди заметки, о которой пользователь хочет получить полную информацию
    """
    note_orm = NotesOrm()
    status_author = check_author(note_orm=note_orm, id_note=id_note)
    if status_author:
        note_info = note_orm.get_note_info_by_id(id_note)
        return render_template('one_note_page.html', title='Заметка', note_data= note_info)
    else:
        return redirect('/notes/')

@notes_router.route('/add_note', methods = ['POST', 'GET'])
@login_required
def add_note_page():
    """
    Получение и обработка формы на добавление новой заметки пользователем
    """
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

@notes_router.route('/update_note/<int:id_note>', methods=['POST', 'GET'])
@login_required
def update_note_page(id_note: int):
    """
    Получение и обработка формы на обновление конкретной заметки
    id_note: айди заметки, которую пользователь хотел бы изменить
    """
    note_orm = NotesOrm()
    status_author = check_author(note_orm=note_orm, id_note=id_note)
    if status_author:
        if request.method == 'POST':
            status_update = update_note_function(note_orm, id_note)
            if status_update == 200:
                return redirect('/notes/')
            else:
                return redirect(f'/notes/update_note/{id_note}')
        else:
            note_info = note_orm.get_note_info_by_id(id_note)
            return render_template('edit_note.html', title='Обновление заметки',
                note_data=note_info)
    else:
        return redirect('/notes/')

@notes_router.route('/delete_note/<int:id_note>')
@login_required
def delete_note_page(id_note: int):
    """
    Обработка запроса на удаления заметки из базы
    id_note: айди заметки, которую пользователь хочет удалить
    """
    note_orm = NotesOrm()
    status_author = check_author(note_orm=note_orm ,id_note=id_note)
    if status_author:
        delete_note_function(note_orm, id_note)
    return redirect('/notes/')
