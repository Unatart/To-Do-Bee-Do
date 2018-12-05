from forms import LoginForm, RegisterForm


def get_login():
    form = LoginForm()

    if form.validate_on_submit():
        status_code = 200
        # login might be email
        username = form.username.data
        password = form.password.data

        return status_code, username, password, form

    return 401, "", "", form


def get_signup():
    form = RegisterForm()

    if form.validate_on_submit():
        status_code = 200
        username = form.username.data
        email = form.email.data
        password = form.password.data

        return status_code, username, email, password, form

    return 401, "", "", form