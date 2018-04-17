from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, BooleanField
from wtforms.validators import InputRequired, URL, EqualTo, Optional
from wtforms_alchemy import Unique, model_form_factory
from wtforms_components import EmailField, Email

from winejournal.data_models.users import User, role_list
from winejournal.extensions import db

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class LoginForm(ModelForm):
    username: StringField('User name', validators=[InputRequired()])
    password: PasswordField('Password', validators=[InputRequired()])


class NewUserForm(ModelForm):
    role_list = role_list()
    username = StringField('Username', validators=[Unique(User.username)])
    email = EmailField('Email Address', validators=[
        InputRequired(),
        Email(),
        Unique(User.email),
        EqualTo('email2', message='Email addresses must match')
    ])
    email2 = EmailField('Confirm Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
        EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm Password')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    display_name = StringField('Display Name')
    image = StringField('Image URL', validators=[URL(), Optional()])
    role = RadioField('Role', choices=role_list, default='member')
    is_enabled = BooleanField('Enabled?')


class EditUserForm(NewUserForm):
    username = StringField('Username')


class DeleteUserForm(ModelForm):
    username = StringField('Username')
