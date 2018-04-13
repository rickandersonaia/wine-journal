from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from flask_login import current_user, login_required

from instance.settings import AWS_DEST_BUCKET, AWS_ENDPOINT, \
    AWS_CLIENT_SECRET_KEY, AWS_CLIENT_ACCESS_KEY, AWS_HOST, JSDEBUG

from winejournal.blueprints.tasting_notes.forms import \
    NewNoteForm, EditNoteForm, DeleteNoteForm

from winejournal.data_models.tastingnotes import TastingNote, \
    tnote_owner_required
from winejournal.data_models.users import admin_required
from winejournal.data_models.wines import Wine
from winejournal.extensions import db

tastingNote = Blueprint('tasting_notes', __name__, template_folder='templates',
                    url_prefix='/tasting-notes')


@tastingNote.route('/', methods=['GET'])
def list_tasting_notes():
    tasting_notes = db.session.query(TastingNote).all()
    return render_template('tasting_notes/region-list.html',
                           tasting_notes=tasting_notes)


@tastingNote.route('/<int:wine_id>/new', methods=['GET', 'POST'])
@login_required
def new_tasting_notes(wine_id):
    wine = db.session.query(Wine).get(wine_id)
    new_tasting_note_form = NewNoteForm()

    if new_tasting_note_form.validate_on_submit():
        note = TastingNote(
            title=new_tasting_note_form.title.data,
            text=new_tasting_note_form.text.data,
            vintage=new_tasting_note_form.vintage.data,
            rating=new_tasting_note_form.rating.data,
            price=new_tasting_note_form.price.data,
            wine_id=wine_id,
            author_id=current_user.id
        )

        db.session.add(note)
        db.session.commit()
        message = 'You added the {} tasting note'.format(note.title)
        flash(message)
        return redirect(url_for('wine.wine_detail', wine_id))

    return render_template('tasting-notes/tasting-note-new.html',
                           form=new_tasting_note_form,
                           wine=wine,
                           AWS_DEST_BUCKET=AWS_DEST_BUCKET,
                           AWS_ENDPOINT=AWS_ENDPOINT,
                           AWS_CLIENT_SECRET_KEY=AWS_CLIENT_SECRET_KEY,
                           AWS_CLIENT_ACCESS_KEY=AWS_CLIENT_ACCESS_KEY,
                           AWS_HOST=AWS_HOST,
                           JSDEBUG=JSDEBUG)


@tastingNote.route('/<int:tnote_id>/', methods=['GET'])
def tasting_notes_detail(tnote_id):
    is_admin = current_user.is_admin()
    is_owner = get_is_owner(tnote_id)
    note = db.session.query(TastingNote).filter_by(id=tnote_id).one()
    data = Prepopulated_Data(region, reg_list)
    print(data)
    return render_template('regions/region-detail.html',
                           region=data,
                           is_admin=is_admin,
                           is_owner=is_owner)


@tastingNote.route('/<int:tnote_id>/edit', methods=['GET', 'POST'])
@tnote_owner_required
def tasting_notes_edit(tnote_id):
    is_admin = current_user.is_admin()
    note = db.session.query(TastingNote).filter_by(id=tnote_id).one()
    parent_id = region.parent_id
    prepopulated_data = Prepopulated_Data(region, reg_list)

    edit_region_form = EditRegionForm(obj=prepopulated_data)

    if request.method == 'POST':
        if edit_region_form.validate_on_submit():
            parentId = get_parent_id(edit_region_form, reg_list)

            region.name = edit_region_form.name.data
            region.description = edit_region_form.description.data
            region.parent_id = parentId
            region.country = edit_region_form.country.data
            region.state = edit_region_form.state.data

            db.session.add(region)
            db.session.commit()
            message = 'You updated the {} region'.format(region.name)
            flash(message)
            return redirect(url_for('regions.list_regions'))

    return render_template('regions/region-edit.html',
                           form=edit_region_form,
                           reg_list=reg_list,
                           parent_id=parent_id,
                           region=region,
                           country_list=country_list,
                           state_list=state_list,
                           is_admin=is_admin)


@tastingNote.route('/<int:region_id>/delete', methods=['GET', 'POST'])
@admin_required
def tasting_notes_delete(region_id):
    region = db.session.query(Region).filter_by(id=region_id).one()
    reg_list = get_sorted_regions()
    data = Prepopulated_Data(region, reg_list)
    delete_region_form = DeleteRegionForm(obj=region)

    if request.method == 'POST':
        if delete_region_form.validate_on_submit():
            db.session.delete(region)
            db.session.commit()
            message = 'You deleted the {} region'.format(region.name)
            flash(message)
            return redirect(url_for('regions.list_regions'))

    return render_template('regions/region-delete.html',
                           region=data,
                           form=delete_region_form)


def get_parent_id(form, reg_list):
    parentId = 0
    if form.parent.data:
        for id, name in reg_list.items():
            if name == form.parent.data:
                parentId = int(id)

    return parentId


class Prepopulated_Data:
    def __init__(self, region, reg_list):

        self.region = region
        self.name = region.name
        self.description = region.description
        self.country = region.country
        self.state = region.state
        self.reg_list = reg_list
        self.parent = self.get_parent_label()

    def get_parent_label(self):
        parent_id = self.region.parent_id
        parentLabel = ''
        if parent_id:
            for id, name in self.reg_list.items():
                if id == parent_id:
                    parentLabel = name

        return parentLabel


def get_is_owner(region_id):
    reg = db.session.query(TastingNote).get(tnote_id)
    if reg.owner == current_user.id:
        return True
    else:
        return False
