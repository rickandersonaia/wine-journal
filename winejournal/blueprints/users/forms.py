from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    username: StringField('User name', validators=[InputRequired()])
    password: PasswordField('Password', validators=[InputRequired()])