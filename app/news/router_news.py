from flask import Blueprint, render_template

news_router = Blueprint('news_router', __name__,
    static_folder='static',
    template_folder='templates/news'                    
    )

@news_router.route('/')
def news_page():
    return render_template('news_page.html', title='Новостная страница')