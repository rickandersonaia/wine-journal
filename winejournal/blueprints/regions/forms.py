from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired


class NewRegionForm(FlaskForm):
    name = StringField('Region name', validators=[InputRequired()])
    description = TextAreaField('Region description')
    parent = StringField('Region parent')
    country = StringField('Country')
    state = StringField('State')


class EditRegionForm(FlaskForm):
    name = StringField('Region name', validators=[InputRequired()])
    description = TextAreaField('Region description')
    parent = StringField('Region parent')
    country = StringField('Country')
    state = StringField('State')


class DeleteRegionForm(FlaskForm):
    parent = StringField('Region parent')
