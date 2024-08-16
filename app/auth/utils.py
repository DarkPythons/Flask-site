

def data_validate(form_data):
    if len(form_data['username']) > 3 and len(form_data['email']) > 5 and "@" in form_data['email']:
        #Если данные валидны
        if form_data['psw'] == form_data['psw2']:
            return 200
        #Если не валидны пароли
        else:
            return 401
    #Если данные в целом не валидны
    else:
        return 400