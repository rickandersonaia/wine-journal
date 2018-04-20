from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import InputRequired


class NewCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[InputRequired()])
    description = TextAreaField('Category description')
    parent = StringField('Category parent')
    image = FileField('Upload an Image')
    delete_image = HiddenField()
    rotate_image = HiddenField()


class EditCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[InputRequired()])
    description = TextAreaField('Category description')
    parent = StringField('Category parent')
    image = FileField('Upload an Image')
    delete_image = HiddenField()
    rotate_image = HiddenField()


class DeleteCategoryForm(FlaskForm):
    parent = StringField('Category parent')
