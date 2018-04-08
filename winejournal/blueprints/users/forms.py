from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import InputRequired
from wtforms_components import EmailField, Email



class LoginForm(FlaskForm):
    username: StringField('User name', validators=[InputRequired()])
    password: PasswordField('Password', validators=[InputRequired()])


class NewUserForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password', validators=[InputRequired()])
    password2 = StringField('Verify Password', validators=[InputRequired()])
    email = EmailField('Email Address', validators=[InputRequired(), Email()])
    email2 = EmailField('Verify Email', validators=[InputRequired()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    display_name = StringField('Display Name')
    image = StringField('Image URL')
    role = StringField('Role')
    is_enabled = BooleanField('Enabled?')


class EditUserForm(FlaskForm):
    username = StringField('Username')

class DeleteUserForm(FlaskForm):
    username = StringField('Username')