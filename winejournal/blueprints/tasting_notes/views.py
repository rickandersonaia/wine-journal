from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from flask_login import current_user, login_required
from flask_uploads import UploadSet, IMAGES

from winejournal.blueprints.media.process_standard_image import \
    ProcessStandardImage
from winejournal.blueprints.s3.views import upload_image
from winejournal.blueprints.tasting_notes.forms import \
    NewNoteForm, EditNoteForm, DeleteNoteForm
from winejournal.data_models.tastingnotes import TastingNote, \
    tnote_owner_required
from winejournal.data_models.users import admin_required
from winejournal.data_models.wines import Wine
from winejournal.extensions import db

tastingNote = Blueprint('tasting_notes', __name__, template_folder='templates',
                        url_prefix='/tasting-notes')

photos = UploadSet('photos', IMAGES)


@tastingNote.route('/', methods=['GET'])
@admin_required
def list_tasting_notes():
    tasting_notes = db.session.query(TastingNote).all()
    return render_template('tasting_notes/tasting-note-list.html',
                           tasting_notes=tasting_notes)


@tastingNote.route('/<int:wine_id>/new', methods=['GET', 'POST'])
@login_required
def new_tasting_note(wine_id):
    wine = db.session.query(Wine).get(wine_id)
    new_tasting_note_form = NewNoteForm()
    img_url = None
    filename = None

    if request.method == 'POST':
        if 'image' in request.files and request.files['image'].filename:
            filename = photos.save(request.files['image'])
            img = ProcessStandardImage(
                filename,  # path to temporary image location
                new_tasting_note_form.rotate_image.data,  # desired rotation
                600  # maximum height or width
            )
            img.process_image()  # saves the modified image to the temp location
        if new_tasting_note_form.validate_on_submit():
            img_url = upload_image(filename)
            note = TastingNote(
                title=new_tasting_note_form.title.data,
                text=new_tasting_note_form.text.data,
                vintage=new_tasting_note_form.vintage.data,
                rating=new_tasting_note_form.rating.data,
                price=new_tasting_note_form.price.data,
                wine_id=wine_id,
                author_id=current_user.id,
                image=img_url
            )

            db.session.add(note)
            db.session.commit()
            message = 'You added the {} tasting note'.format(note.title)
            flash(message)
            return redirect(url_for('wines.wine_detail', wine_id=wine_id))

    return render_template('tasting_notes/tasting-note-new.html',
                           form=new_tasting_note_form,
                           wine=wine)


@tastingNote.route('/<int:tnote_id>/', methods=['GET'])
@login_required
def tasting_notes_detail(tnote_id):
    is_admin = current_user.is_admin()
    is_owner = get_is_owner(tnote_id)
    note = db.session.query(TastingNote).filter_by(id=tnote_id).one()
    return render_template('tasting_notes/tasting-note-detail.html',
                           note=note,
                           is_admin=is_admin,
                           is_owner=is_owner)


@tastingNote.route('/<int:tnote_id>/edit', methods=['GET', 'POST'])
@tnote_owner_required
def tasting_notes_edit(tnote_id):
    is_admin = current_user.is_admin()
    note = db.session.query(TastingNote).filter_by(id=tnote_id).one()
    wine = db.session.query(Wine).get(note.wine_id)
    img_url = None
    filename = None

    edit_tasting_note_form = EditNoteForm(obj=note)

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

            note.title = edit_tasting_note_form.title.data
            note.text = edit_tasting_note_form.text.data
            note.vintage = edit_tasting_note_form.vintage.data
            note.rating = edit_tasting_note_form.rating.data
            note.price = edit_tasting_note_form.price.data
            if img_url:
                note.image = img_url
            else:
                if edit_tasting_note_form.delete_image.data == "true":
                    note.image = ''

            db.session.add(note)
            db.session.commit()
            message = 'You updated the {} tasting note'.format(wine.name)
            flash(message)
            return redirect(url_for('wines.wine_detail', wine_id=wine.id))

    return render_template('tasting_notes/tasting-note-edit.html',
                           form=edit_tasting_note_form,
                           note=note,
                           wine=wine,
                           is_admin=is_admin)


@tastingNote.route('/<int:tnote_id>/delete', methods=['GET', 'POST'])
@admin_required
def tasting_notes_delete(tnote_id):
    note = db.session.query(TastingNote).filter_by(id=tnote_id).one()

    wine = db.session.query(Wine).get(note.wine_id)
    delete_note_form = DeleteNoteForm(obj=note)

    if request.method == 'POST':
        if delete_note_form.validate_on_submit():
            db.session.delete(note)
            db.session.commit()
            message = 'You deleted the {} tasting note'.format(wine.name)
            flash(message)
            return redirect(url_for('wines.wine_detail', wine_id=wine.id))

    return render_template('tasting_notes/tasting-note-delete.html',
                           wine=wine,
                           note=note,
                           form=delete_note_form)


def get_is_owner(tnote_id):
    reg = db.session.query(TastingNote).get(tnote_id)
    if reg.author_id == current_user.id:
        return True
    else:
        return False
