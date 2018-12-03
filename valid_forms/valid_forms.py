from forms import LoginForm, RegisterForm
from validator.validator import Validator

def valid_login():
    form = LoginForm()

    if form.validate_on_submit():
        if Validator.validate_username(form.username.data) == True:
            status_code = 200
            username = form.username.data
            password = form.password.data

            return status_code, username, password, form

    return 403, "", "", form

def valid_signup():
    pass