from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms_components import IntegerSliderField
from wtforms.validators import InputRequired


class NewWineForm(FlaskForm):
    name = StringField('Wine name', validators=[InputRequired()])
    maker = StringField('Wine maker', validators=[InputRequired()])
    vintage = IntegerField('Vintage')
    price = IntegerSliderField('Price Range')
    description = TextAreaField('Wine description')
    category = StringField('Wine category')
    region = StringField('Wine region')


class EditWineForm(FlaskForm):
    name = StringField('Wine name', validators=[InputRequired()])
    maker = StringField('Wine maker', validators=[InputRequired()])
    vintgage = IntegerField('Vintage')
    price = IntegerSliderField('Price Range')
    description = TextAreaField('Wine description')
    category = StringField('Wine category')
    region = StringField('Wine region')

class DeleteWineForm(FlaskForm):
    region = StringField('Wine region')