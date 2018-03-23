from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField


class NewCategoryForm(FlaskForm):
    name = StringField('name')
    description = StringField('description')
    parent = StringField('parent')