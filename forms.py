from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Email, Length, Regexp, EqualTo
import re
from models.models import User

EMAIL_REGEX = re.compile(r'^\S+@\S+\.\S+$')
USERNAME_REGEX = re.compile(r'^\S+$')


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email')
    username = StringField('username')
    # password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=20)])
    password = PasswordField('password')


# def validate_email(self, field):
#     if User.query.filter_by(email=field.data).first():
#         raise ValidationError('Email already registered.')
#
#
# def validate_username(self, field):
#     if User.query.filter_by(username=field.data).first():
#         raise ValidationError('Username already in use.')