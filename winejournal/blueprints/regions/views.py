from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from flask_login import current_user, login_required
from flask_uploads import UploadSet, IMAGES

from winejournal.blueprints.regions.country_list import Countries
from winejournal.blueprints.regions.forms import \
    NewRegionForm, EditRegionForm, DeleteRegionForm
from winejournal.blueprints.regions.sorted_list import \
    get_sorted_regions
from winejournal.blueprints.s3.views import upload_image
from winejournal.data_models.regions import Region, region_owner_required
from winejournal.data_models.users import admin_required
from winejournal.data_models.wines import Wine
from winejournal.extensions import db

regions = Blueprint('regions', __name__, template_folder='templates',
                    url_prefix='/regions')

photos = UploadSet('photos', IMAGES)


@regions.route('/', methods=['GET'])
def list_regions():
    region_list = get_sorted_regions()
    return render_template('regions/region-list.html',
                           region_list=region_list)


@regions.route('/new', methods=['GET', 'POST'])
@login_required
def new_region():
    reg_list = get_sorted_regions()
    country_list = Countries.country_list('')
    state_list = Countries.state_list('')
    new_region_form = NewRegionForm()
    img_url = None
    filename = None

    if request.method == 'POST':
        if 'image' in request.files and request.files['image'].filename:
            filename = photos.save(request.files['image'])
        if new_region_form.validate_on_submit():
            parentId = 0
            if new_region_form.parent.data:
                for id, name in reg_list.items():
                    if name == new_region_form.parent.data:
                        parentId = int(id)

            img_url = upload_image(filename)
            region = Region(
                name=new_region_form.name.data,
                description=new_region_form.description.data,
                parent_id=parentId,
                country=new_region_form.country.data,
                state=new_region_form.state.data,
                owner=current_user.id,
                image=img_url
            )

            db.session.add(region)
            db.session.commit()
            message = 'You added the {} region'.format(region.name)
            flash(message)
            return redirect(url_for('regions.list_regions'))

    return render_template('regions/region-new.html',
                           form=new_region_form,
                           reg_list=reg_list,
                           country_list=country_list,
                           state_list=state_list)


@regions.route('/<int:region_id>/', methods=['GET'])
def region_detail(region_id):
    if current_user.is_authenticated:
        display_name = current_user.displayName()
        avatar = current_user.avatar()
        is_admin = current_user.is_admin()
        is_owner = get_is_owner(region_id)
    else:
        display_name = None
        avatar = None
        is_admin = False
        is_owner = False
    reg_list = get_sorted_regions()
    region = db.session.query(Region).filter_by(id=region_id).one()
    wine_list = db.session.query(Wine).filter_by(region=region_id).all()
    data = Prepopulated_Data(region, reg_list)
    print(data)
    return render_template('regions/region-detail.html',
                           region=data,
                           is_admin=is_admin,
                           is_owner=is_owner,
                           wine_list=wine_list)


@regions.route('/<int:region_id>/edit', methods=['GET', 'POST'])
@region_owner_required
def region_edit(region_id):
    is_admin = current_user.is_admin()
    reg_list = get_sorted_regions()
    country_list = Countries.country_list(region_id)
    state_list = Countries.state_list(region_id)
    region = db.session.query(Region).filter_by(id=region_id).one()
    parent_id = region.parent_id
    prepopulated_data = Prepopulated_Data(region, reg_list)

    edit_region_form = EditRegionForm(obj=prepopulated_data)

    img_url = None
    filename = None

    if request.method == 'POST':
        if 'image' in request.files and request.files['image'].filename:
            filename = photos.save(request.files['image'])
            if edit_region_form.validate_on_submit():
                parentId = get_parent_id(edit_region_form, reg_list)

                img_url = upload_image(filename)

                region.name = edit_region_form.name.data
                region.description = edit_region_form.description.data
                region.parent_id = parentId
                region.country = edit_region_form.country.data
                region.state = edit_region_form.state.data
                region.image = img_url

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


@regions.route('/<int:region_id>/delete', methods=['GET', 'POST'])
@admin_required
def region_delete(region_id):
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
        self.image = region.image

    def get_parent_label(self):
        parent_id = self.region.parent_id
        parentLabel = ''
        if parent_id:
            for id, name in self.reg_list.items():
                if id == parent_id:
                    parentLabel = name

        return parentLabel


def get_is_owner(region_id):
    reg = db.session.query(Region).get(region_id)
    if reg.owner == current_user.id:
        return True
    else:
        return False
