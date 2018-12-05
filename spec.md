### Спецификация приложения:

Приложение ToDo List - приложение для создания заметок и дел, которые необходимо выполнить.

В приложении можно :
1. Зарегистрироваться
2. Выполнить авторизацию
3. Добавить заметку
4. Поменить заметку как выполненную\ невыполненную
5. Удалить заметку 

Вид данных:
    
  - Username  
   
        4 < username.len() < 20      
        for key in username:
            if not str(key).isalpha() and key not in "_." and not '0' <= key <= '9':
                return False
        return True
        
  - Email
  
        email_validator
        
  - Password
  
        4 < password.len() < 20

Приложение написано на языке программирования Python3

В качестве сервера используется Flask, в качестве базы данных SQLite вместе с ORM - SQLAlchemy 

##### Тестируемые методы и возвращаемые статусы

###### Авторизация
- возвращает код 200 OK если форма пуста и не была заполнена(первое попадание на страницу)
- возвращает код 302 FOUND если форма заполнена без проблем и совершен редирект на страницу с списком дел (УСПЕХ)
- возвращает код 401 UNAUTHORIZED если форма заполнена с ошибками, либо в базе нет такой записи (НЕУДАЧА)


        @app.route('/login', methods=['GET', 'POST'])
        def login():
        status_code, username, password, form = get_login()   
            if status_code == 200:
                try:
                    username, password, id, status_code = db_manager.login(username, password)
                    if status_code == 200:
                        session['id'] = id
                        return redirect(url_for('board'))
                    elif status_code == 401:
                        return render_template('login.html', error='Invalid data, try again or SignUp',
                                               form=form), status.HTTP_401_UNAUTHORIZED

                except sqlalchemy.exc.SQLAlchemyError:
                    abort(500)

        return render_template('login.html', form=form), status.HTTP_200_OK



###### Регистрация
- возвращает код 200 OK если форма пуста и не была заполнена(первое попадание на страницу)
- возвращает код 302 FOUND если форма заполнена без проблем и совершен редирект на страницу с списком дел (УСПЕХ)
- возвращает код 409 CONFLICT если форма заполнена с ошибками, либо в базе уже существует запись с таким username или email (НЕУДАЧА)


        @app.route('/signup', methods=['GET', 'POST'])
        def signup():
            status_code, username, email, password, form = get_signup()
            if status_code == 200:
                    username, email, password, id, status_code, error_identity = \
                        db_manager.create_user(username, email, password)
                    if status_code == 409:
                        if error_identity == 'login':
                            return render_template('signup.html', form=form,
                                                   error='Incorrect username'), status.HTTP_409_CONFLICT
                        if error_identity == 'email':
                            return render_template('signup.html', form=form,
                                                   error='Incorrect email'), status.HTTP_409_CONFLICT
                        if error_identity == 'password':
                            return render_template('signup.html', form=form,
                                                   error='Incorrect password'), status.HTTP_409_CONFLICT
                    else:
                        session['id'] = id
                        return redirect(url_for('board'))

        return render_template('signup.html', form=form), status.HTTP_200_OK
