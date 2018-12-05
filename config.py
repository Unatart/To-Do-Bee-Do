from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/unatart/TodoList/backenddb/backend.sqlite'
app.config.from_object('config')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
db.drop_all()
db.create_all()
#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
