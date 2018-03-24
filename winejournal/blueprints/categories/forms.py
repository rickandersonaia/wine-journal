from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired


class NewCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[InputRequired()])
    description = TextAreaField('Category description')
    parent = StringField('Category parent')
