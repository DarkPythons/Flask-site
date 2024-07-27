from flask import Blueprint, render_template

router_auth = Blueprint('router_auth', __name__, static_folder='static', template_folder='templates')


@router_auth.route('/login')
def register():
    return render_template('auth/login.html', title='Вход')
