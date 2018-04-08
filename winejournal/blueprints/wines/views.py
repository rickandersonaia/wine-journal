from flask import Blueprint, render_template, redirect, url_for, \
    flash, request

from winejournal.blueprints.wines.forms import \
    NewWineForm, EditWineForm, DeleteWineForm
from winejournal.blueprints.categories.sorted_list import \
    get_sorted_categories
from winejournal.blueprints.regions.sorted_list import \
    get_sorted_regions
from winejournal.data_models.wines import Wine
from winejournal.data_models.regions import Region
from winejournal.data_models.categories import Category
from winejournal.extensions import db


wines = Blueprint('wines', __name__, template_folder='templates',
                       url_prefix='/wine')


@wines.route('/', methods=['GET'])
def list_wines():
    wine_list = db.session.query(Wine).all()
    return render_template('wines/wine-list.html',
                           wine_list=wine_list)


@wines.route('/new', methods=['GET', 'POST'])
def new_wine():
    cat_list = get_sorted_categories()
    reg_list = get_sorted_regions()
    new_wine_form = NewWineForm()
    if new_wine_form.validate_on_submit():
        categoryId = get_category_id(new_wine_form.category.data, cat_list)
        regionId = get_region_id(new_wine_form.region.data, reg_list)
        wine = Wine(
            name=new_wine_form.name.data,
            maker=new_wine_form.maker.data,
            vintage=new_wine_form.vintage.data,
            price=new_wine_form.price.data,
            description=new_wine_form.description.data,
            category=categoryId,
            region=regionId,
            owner='1'
        )

        db.session.add(wine)
        db.session.commit()
        message = 'You added {} to the journal'.format(wine.name)
        flash(message)
        return redirect(url_for('wines.list_wines'))

    return render_template('wines/wine-new.html',
                           form=new_wine_form,
                           cat_list=cat_list,
                           reg_list=reg_list)


@wines.route('/<int:wine_id>/', methods=['GET'])
def wine_detail(wine_id):
    wine = db.session.query(Wine).filter_by(id=wine_id).one()
    region = db.session.query(Region).filter_by(id=wine.region).one()
    category = db.session.query(Category).filter_by(id=wine.category)
    price = get_dollar_signs(wine)
    return render_template('wines/wine-detail.html',
                           wine=wine,
                           region=region,
                           category=category,
                           price=price)


@wines.route('/<int:wine_id>/edit', methods=['GET', 'POST'])
def wine_edit(wine_id):
    cat_list = get_sorted_categories()
    reg_list = get_sorted_regions()
    wine = db.session.query(Wine).filter_by(id=wine_id).one()
    prepopulated_data = Formatted_Data(wine, cat_list, reg_list)

    edit_wine_form = EditWineForm(obj=prepopulated_data)

    if request.method == 'POST':
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

            db.session.add(wine)
            db.session.commit()
            message = 'You updated the {} wine'.format(wine.name)
            flash(message)
            return redirect(url_for('wines.list_wines'))

    return render_template('wines/wine-edit.html',
                           form=edit_wine_form,
                           cat_list=cat_list,
                           reg_list=reg_list,
                           wine=wine)


@wines.route('/<int:wine_id>/delete', methods=['GET', 'POST'])
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
    priceLabel = dollar_signs[wine.price]
    return priceLabel
