from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import InputRequired
from wtforms_components import IntegerSliderField


class NewWineForm(FlaskForm):
    name = StringField('Wine name', validators=[InputRequired()])
    maker = StringField('Wine maker', validators=[InputRequired()])
    vintage = IntegerField('Vintage')
    price = IntegerSliderField('Price Range')
    description = TextAreaField('Wine description')
    category = StringField('Wine category', validators=[InputRequired()])
    region = StringField('Wine region', validators=[InputRequired()])
    image = FileField('Upload an Image')
    delete_image = HiddenField()
    rotate_image = HiddenField()
    image_url = HiddenField()


class EditWineForm(FlaskForm):
    name = StringField('Wine name', validators=[InputRequired()])
    maker = StringField('Wine maker', validators=[InputRequired()])
    vintage = IntegerField('Vintage')
    price = IntegerSliderField('Price Range')
    description = TextAreaField('Wine description')
    category = StringField('Wine category', validators=[InputRequired()])
    region = StringField('Wine region', validators=[InputRequired()])
    owner = IntegerField('Owner')
    image = FileField('Upload an Image')
    delete_image = HiddenField()
    rotate_image = HiddenField()
    image_url = HiddenField()


class DeleteWineForm(FlaskForm):
    region = StringField('Wine region')
