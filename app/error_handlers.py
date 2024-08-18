from flask import Blueprint

error_router = Blueprint('error_handlers', 
    __name__, 
    static_folder='static', 
    template_folder='template_error')

@error_router.app_errorhandler(404)
def handler404(error):
    
    return ("страница не найдена", 404)