from flask import Blueprint, render_template, request, flash


#orm = GetConnectOrm()


router = Blueprint('router_auth', __name__, static_folder='static', template_folder='templates')


@router.route('/login')
def login():
    return render_template('auth/login.html', title='Вход')

def data_validate(form_data):
    if len(form_data['username']) > 3 and len(form_data['email']) > 5 and "@" in form_data['email']:
        if form_data['psw'] == form_data['psw2']:
            return 200
        else:
            return 401
    else:
        return 400

@router.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if data_validate(request.form) == 200:
            try:
                orm.register_user(request.form['username'], request.form['email'], request.form['psw'])
            except Exception as error:
                #Откат базы данных в случае ошибки
                orm.get_rollback()
                flash('Ошибка на стороне базы данных')
                print('Ошибка на стороне базы данных: ' + str(error))
        elif data_validate(request.form) == 400:
            flash("Неккоректные email или username.s")
        else:
            flash('Пароли не совпадают.')

        
    return render_template('auth/register.html', title='Регистрация')