from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import TextAreaField, IntegerField, HiddenField
from wtforms.validators import InputRequired


class NewCommentForm(FlaskForm):
    text = TextAreaField('Tasting Notes', validators=[InputRequired()])
    image = FileField('Upload an Image')
    author_id = IntegerField('Author ID')
    tnote_id = IntegerField('Tasting Note ID')
    delete_image = HiddenField()
    rotate_image = HiddenField()


class EditCommentorm(FlaskForm):
    text = TextAreaField('Tasting Notes', validators=[InputRequired()])
    image = FileField('Upload an Image')
    author_id = IntegerField('Author ID')
    tnote_id = IntegerField('Tasting Note ID')
    delete_image = HiddenField()
    rotate_image = HiddenField()


class DeleteCommentForm(FlaskForm):
    author_id = IntegerField('Author ID')
