from flask import Blueprint, request, render_template, flash

converter_router = Blueprint('converter_router', __name__,
    static_folder='static', 
    template_folder='templates')

@converter_router.route('/', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        pass
    return render_template('converter/converter_page.html')