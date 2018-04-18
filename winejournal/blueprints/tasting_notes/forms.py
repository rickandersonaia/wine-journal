from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, IntegerField, RadioField, HiddenField
from wtforms.validators import InputRequired
from wtforms_components import IntegerSliderField


class NewNoteForm(FlaskForm):
    title = StringField('Tasting Note Title', validators=[InputRequired()])
    text = TextAreaField('Tasting Notes', validators=[InputRequired()])
    price = StringField('Purchase Price?')
    vintage = IntegerField('Vintage')
    rating = IntegerSliderField('Rating')
    image = FileField('Upload an Image')
    delete_image = HiddenField()
    rotate_image = HiddenField()


class EditNoteForm(FlaskForm):
    title = StringField('Tasting Note Title', validators=[InputRequired()])
    text = TextAreaField('Tasting Notes', validators=[InputRequired()])
    price = StringField('Purchase Price?')
    vintage = IntegerField('Vintage')
    rating = IntegerSliderField('Rating')
    image = FileField('Upload an Image')
    delete_image = HiddenField()
    rotate_image = HiddenField()

class DeleteNoteForm(FlaskForm):
    title = StringField('Tasting Note Title')