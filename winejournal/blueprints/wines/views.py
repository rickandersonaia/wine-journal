from flask import Blueprint, render_template, redirect, url_for, \
    flash, request, jsonify
from flask_login import current_user, login_required
from flask_uploads import UploadSet, IMAGES

from config.settings import DEFAULT_WINE_IMAGE
from winejournal.blueprints.categories.sorted_list import \
    get_sorted_categories
from winejournal.blueprints.media.process_standard_image import \
    ProcessStandardImage
from winejournal.blueprints.regions.sorted_list import \
    get_sorted_regions
from winejournal.blueprints.s3.views import upload_image
from winejournal.blueprints.wines.forms import \
    NewWineForm, EditWineForm, DeleteWineForm
from winejournal.data_models.categories import Category
from winejournal.data_models.regions import Region
from winejournal.data_models.users import admin_required
from winejournal.data_models.wines import Wine, wine_owner_required
from winejournal.extensions import db, csrf

wines = Blueprint('wines', __name__, template_folder='templates',
                  url_prefix='/wine')

photos = UploadSet('photos', IMAGES)


@wines.route('/', methods=['GET'])
def list_wines():
    wine_list = db.session.query(Wine).all()
    return render_template('wines/wine-list.html',
                           wine_list=wine_list)


@wines.route('/new', methods=['GET', 'POST'])
@login_required
def new_wine():
    cat_list = get_sorted_categories()
    reg_list = get_sorted_regions()
    new_wine_form = NewWineForm()
    img_url = None
    filename = None

    if request.method == 'POST':
        if 'image' in request.files and request.files['image'].filename:
            filename = photos.save(request.files['image'])
            img = ProcessStandardImage(
                filename,  # path to temporary image location
                new_wine_form.rotate_image.data,  # desired rotation
                600  # maximum height or width
            )
            img.process_image()  # saves the modified image to the temp location
        if new_wine_form.validate_on_submit():
            categoryId = get_category_id(new_wine_form.category.data, cat_list)
            regionId = get_region_id(new_wine_form.region.data, reg_list)
            img_url = upload_image(filename)
            if img_url == None:
                img_url = DEFAULT_WINE_IMAGE

            wine = Wine(
                name=new_wine_form.name.data,
                maker=new_wine_form.maker.data,
                vintage=new_wine_form.vintage.data,
                price=new_wine_form.price.data,
                description=new_wine_form.description.data,
                category=categoryId,
                region=regionId,
                owner=current_user.id,
                image=img_url
            )

            db.session.add(wine)
            db.session.commit()
            message = 'You added {} to the journal'.format(wine.name)
            flash(message)
            return redirect(url_for('wines.list_wines'))

    return render_template('wines/wine-new.html',
                           form=new_wine_form,
                           cat_list=cat_list,
                           reg_list=reg_list,
                           img_url=img_url)


@wines.route('/<int:wine_id>/', methods=['GET'])
def wine_detail(wine_id):
    if current_user.is_authenticated:
        display_name = current_user.displayName()
        avatar = current_user.avatar()
        is_admin = current_user.is_admin()
        is_owner = get_is_owner(wine_id)
    else:
        display_name = None
        avatar = None
        is_admin = False
        is_owner = False

    wine = db.session.query(Wine).get(wine_id)
    region = db.session.query(Region).get(wine.region)
    category = db.session.query(Category).get(wine.category)
    price = get_dollar_signs(wine)
    return render_template('wines/wine-detail.html',
                           wine=wine,
                           region=region,
                           category=category,
                           price=price,
                           is_admin=is_admin,
                           is_owner=is_owner,
                           display_name=display_name,
                           avatar=avatar)


@wines.route('/<int:wine_id>/edit', methods=['GET', 'POST'])
@wine_owner_required
def wine_edit(wine_id):
    is_admin = current_user.is_admin()
    cat_list = get_sorted_categories()
    reg_list = get_sorted_regions()
    wine = db.session.query(Wine).get(wine_id)
    prepopulated_data = Formatted_Data(wine, cat_list, reg_list)
    edit_wine_form = EditWineForm(obj=prepopulated_data)

    img_url = None
    filename = None

    if request.method == 'POST':
        if 'image' in request.files and request.files['image'].filename:
            filename = photos.save(request.files['image'])
            img = ProcessStandardImage(
                filename,  # path to temporary image location
                edit_wine_form.rotate_image.data,  # desired rotation
                600  # maximum height or width
            )
            img.process_image()  # saves the modified image to the temp location
            # img_url = edit_wine_form.image_url.data
            img_url = upload_image(filename)

        if edit_wine_form.validate_on_submit():
            categoryId = get_category_id(edit_wine_form.category.data, cat_list)
            regionId = get_region_id(edit_wine_form.region.data, reg_list)

            wine.name = edit_wine_form.name.data
            wine.maker = edit_wine_form.maker.data
            wine.vintage = edit_wine_form.vintage.data
            wine.price = edit_wine_form.price.data
            wine.description = edit_wine_form.description.data
            wine.region = regionId
            wine.category = categoryId
            wine.owner = edit_wine_form.owner.data
            if img_url:
                wine.image = img_url
            else:
                if edit_wine_form.delete_image.data == "true":
                    wine.image = DEFAULT_WINE_IMAGE

            db.session.add(wine)
            db.session.commit()
            message = 'You updated the {} wine'.format(wine.name)
            flash(message)
            return redirect(url_for('wines.list_wines'))

    return render_template('wines/wine-edit.html',
                           form=edit_wine_form,
                           cat_list=cat_list,
                           reg_list=reg_list,
                           wine=wine,
                           is_admin=is_admin)


@wines.route('/<int:wine_id>/delete', methods=['GET', 'POST'])
@admin_required
def wine_delete(wine_id):
    wine = db.session.query(Wine).filter_by(id=wine_id).one()
    region = db.session.query(Region).filter_by(id=wine.region).one()
    category = db.session.query(Category).filter_by(id=wine.category)
    price = get_dollar_signs(wine)
    delete_wine_form = DeleteWineForm(obj=wine)

    if request.method == 'POST':
        if delete_wine_form.validate_on_submit():
            db.session.delete(wine)
            db.session.commit()
            message = 'You deleted the {} wine'.format(wine.name)
            flash(message)
            return redirect(url_for('wines.list_wines'))

    return render_template('wines/wine-delete.html',
                           form=delete_wine_form,
                           wine=wine,
                           region=region,
                           category=category,
                           price=price)


class Formatted_Data:
    def __init__(self, wine, cat_list, reg_list):

        self.wine = wine
        self.cat_list = cat_list
        self.reg_list = reg_list
        self.name = wine.name
        self.maker = wine.maker
        self.vintage = wine.vintage
        self.price = wine.price
        self.description = wine.description
        self.category = self.get_category_label()
        self.region = self.get_region_label()
        self.owner = wine.owner
        self.image = wine.image

    def get_category_label(self):
        category_id = self.wine.category
        categoryLabel = ''
        if category_id:
            for id, name in self.cat_list.items():
                if id == category_id:
                    categoryLabel = name

        return categoryLabel

    def get_region_label(self):
        region_id = self.wine.region
        regionLabel = ''
        if region_id:
            for id, name in self.reg_list.items():
                if id == region_id:
                    regionLabel = name

        return regionLabel


def get_category_id(category, cat_list):
    categoryId = ''
    if category:
        for id, name in cat_list.items():
            if name == category:
                categoryId = int(id)
    return categoryId


def get_region_id(region, reg_list):
    regionId = ''
    if region:
        for id, name in reg_list.items():
            # print(id, name, region)
            if name == region:
                regionId = int(id)

    # print(regionId)
    return regionId


def get_dollar_signs(wine):
    dollar_signs = ['Not known', '$', '$$', '$$$', '$$$$', '$$$$$']
    priceLabel = ''
    if wine.price:
        priceLabel = dollar_signs[wine.price]
    else:
        priceLabel = 'Not known'
    return priceLabel


def get_is_owner(wine_id):
    wine = db.session.query(Wine).get(wine_id)
    if wine.owner == current_user.id:
        return True
    else:
        return False


# API Routes

@wines.route('/api/v1/wines/', methods=['GET'])
@login_required
@csrf.exempt
def api_list_wines():
    wines = db.session.query(Wine).all()
    return jsonify(
        AllTastingNotes=[wines.serialize for wine in
                         wines])


@wines.route('/api/v1/<int:wine_id>/', methods=['GET'])
@login_required
@csrf.exempt
def api_wine_detail(wine_id):
    wine = db.session.query(Wine).get(wine_id)
    return jsonify(Region=[wine.serialize])
