"""
Модуль для вынесения разных функций из основной программы,
для улучшения читабельности.
"""

def data_validate(form_data):
    if len(form_data['username']) > 3 and len(form_data['email']) > 5 and "@" in form_data['email']:
        if form_data['psw'] == form_data['psw2']:
            return 200
        else:
            return 401
    else:
        return 400
    

def creating_dict_for_profile(user_orm):
    date = {
        "username" : user_orm['username'],
        "email" : user_orm['email'],
        "date" : user_orm['date']
    }
    return date