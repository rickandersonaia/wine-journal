from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import InputRequired


class NewRegionForm(FlaskForm):
    name = StringField('Region name', validators=[InputRequired()])
    description = TextAreaField('Region description')
    parent = StringField('Region parent')
    country = StringField('Country')
    state = StringField('State')
    image = FileField('Upload an Image')
    delete_image = HiddenField()


class EditRegionForm(FlaskForm):
    name = StringField('Region name', validators=[InputRequired()])
    description = TextAreaField('Region description')
    parent = StringField('Region parent')
    country = StringField('Country')
    state = StringField('State')
    image = FileField('Upload an Image')
    delete_image = HiddenField()


class DeleteRegionForm(FlaskForm):
    parent = StringField('Region parent')
