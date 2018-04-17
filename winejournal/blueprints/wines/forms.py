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
    category = StringField('Wine category')
    region = StringField('Wine region')
    image = FileField('Upload an Image')
    delete_image = HiddenField()


class EditWineForm(FlaskForm):
    name = StringField('Wine name', validators=[InputRequired()])
    maker = StringField('Wine maker', validators=[InputRequired()])
    vintage = IntegerField('Vintage')
    price = IntegerSliderField('Price Range')
    description = TextAreaField('Wine description')
    category = StringField('Wine category')
    region = StringField('Wine region')
    owner = IntegerField('Owner')
    image = FileField('Upload an Image')
    delete_image = HiddenField()


class DeleteWineForm(FlaskForm):
    region = StringField('Wine region')
