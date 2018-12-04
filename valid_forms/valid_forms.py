from forms import LoginForm, RegisterForm
from validator.validator import Validator

def valid_login():
    form = LoginForm()

    if form.validate_on_submit():
        if Validator.validate_username(form.username.data) == True \
                or Validator.validate_email(form.username.data) == True:
            status_code = 200
            # login might be email
            username = form.username.data
            password = form.password.data

            return status_code, username, password, form

    return 401, "", "", form

def valid_signup():
    form = RegisterForm()

    if form.validate_on_submit():
        if Validator.validate_username(form.username.data) == True and \
            Validator.validate_email(form.email.data) == True and \
            Validator.validate_password(form.password.data) == True:
            status_code = 200
            username = form.username.data
            email = form.email.data
            password = form.password.data

            return status_code, username, email, password, form

    return 400, "", "", "", form