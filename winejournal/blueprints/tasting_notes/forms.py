from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, RadioField
from wtforms.validators import InputRequired
from wtforms_components import IntegerSliderField


class NewNoteForm(FlaskForm):
    title = StringField('Tasting Note Title', validators=[InputRequired()])
    text = TextAreaField('Tasting Notes', validators=[InputRequired()])
    price = StringField('Purchase Price?')
    vintage = IntegerField('Vintage')
    rating = IntegerSliderField('Rating')


class EditNoteForm(FlaskForm):
    title = StringField('Tasting Note Title', validators=[InputRequired()])
    text = TextAreaField('Tasting Notes', validators=[InputRequired()])
    price = StringField('Purchase Price?')
    vintage = IntegerField('Vintage')
    rating = IntegerSliderField('Rating')

class DeleteNoteForm(FlaskForm):
    parent = StringField('Region parent')