from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from flask_login import current_user, login_required
from flask_uploads import UploadSet, IMAGES

from winejournal.blueprints.comments.forms import \
    NewCommentForm, EditCommentorm, DeleteCommentForm
from winejournal.blueprints.media.process_standard_image import \
    ProcessStandardImage
from winejournal.blueprints.s3.views import upload_image
from winejournal.data_models.comments import Comment, \
    comment_owner_required
from winejournal.data_models.tastingnotes import TastingNote
from winejournal.data_models.users import admin_required
from winejournal.extensions import db

comment = Blueprint('comment', __name__, template_folder='templates',
                    url_prefix='/comment')

photos = UploadSet('photos', IMAGES)


@comment.route('/', methods=['GET'])
@admin_required
def list_comments():
    comments = db.session.query(Comment).all()
    return render_template('comments/comment-list.html',
                           comments=comments)


@comment.route('/<int:tnote_id>/new', methods=['GET', 'POST'])
@login_required
def new_comment(tnote_id):
    tnote = db.session.query(TastingNote).get(tnote_id)
    new_comment_form = NewCommentForm()
    img_url = None
    filename = None

    if request.method == 'POST':
        if 'image' in request.files and request.files['image'].filename:
            filename = photos.save(request.files['image'])
            img = ProcessStandardImage(
                filename,  # path to temporary image location
                new_comment_form.rotate_image.data,  # desired rotation
                600  # maximum height or width
            )
            img.process_image()  # saves the modified image to the temp location
        if new_comment_form.validate_on_submit():
            img_url = upload_image(filename)
            comment = Comment(
                text=new_comment_form.text.data,
                tnote_id=tnote_id,
                author_id=current_user.id,
                image=img_url
            )

            db.session.add(comment)
            db.session.commit()
            message = 'You added a comment to the {} tasting note'.format(
                tnote.title)
            flash(message)
            return redirect(url_for('wines.wine_detail', wine_id=tnote.wine_id))

    return render_template('comments/comment-new.html',
                           form=new_comment_form,
                           tnote=tnote)


@comment.route('/<int:comment_id>/', methods=['GET'])
@login_required
def comment_detail(comment_id):
    is_admin = current_user.is_admin()
    is_owner = get_is_owner(comment_id)
    comment = db.session.query(Comment).get(comment_id)
    return render_template('comments/comment-detail.html',
                           comment=comment,
                           is_admin=is_admin,
                           is_owner=is_owner)


@comment.route('/<int:comment_id>/edit', methods=['GET', 'POST'])
@comment_owner_required
def comment_edit(comment_id):
    is_admin = current_user.is_admin()
    comment = db.session.query(Comment).get(comment_id)
    img_url = None
    filename = None

    edit_tasting_note_form = EditCommentorm(obj=comment)

    if request.method == 'POST':
        if 'image' in request.files and request.files['image'].filename:
            filename = photos.save(request.files['image'])
            img = ProcessStandardImage(
                filename,  # path to temporary image location
                edit_tasting_note_form.rotate_image.data,  # desired rotation
                600  # maximum height or width
            )
            img.process_image()  # saves the modified image to the temp location
        if edit_tasting_note_form.validate_on_submit():
            img_url = upload_image(filename)  # moves image from temp to S3
            comment.text = edit_tasting_note_form.text.data
            comment.author_id = edit_tasting_note_form.author_id.data
            comment.tnote_id = edit_tasting_note_form.tnote_id.data
            if img_url:
                comment.image = img_url
            else:
                if edit_tasting_note_form.delete_image.data == "true":
                    comment.image = ''

            db.session.add(comment)
            db.session.commit()
            message = 'You updated your comment about the {} tasting note'\
                .format(comment.tasting_note.title)
            flash(message)
            return redirect(url_for('wines.wine_detail',
                                    wine_id=comment.tasting_note.wine_id))

    return render_template('comments/comment-edit.html',
                           form=edit_tasting_note_form,
                           is_admin=is_admin,
                           comment=comment)


@comment.route('/<int:comment_id>/delete', methods=['GET', 'POST'])
@admin_required
def comments_delete(comment_id):
    comment = db.session.query(Comment).get(comment_id)
    delete_comment_form = DeleteCommentForm(obj=comment)

    if request.method == 'POST':
        if delete_comment_form.validate_on_submit():
            db.session.delete(comment)
            db.session.commit()
            message = 'You deleted your comment on {}\'s tasting note'.format(
                comment.tasting_note.user.first_name)
            flash(message)
            return redirect(url_for('wines.wine_detail',
                                    wine_id=comment.tasting_note.wine_id))

    return render_template('comments/comment-delete.html',
                           form=delete_comment_form,
                           comment=comment)


def get_is_owner(comment_id):
    comm = db.session.query(Comment).get(comment_id)
    if comm.author_id == current_user.id:
        return True
    else:
        return False
