from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from sqlalchemy.orm import sessionmaker

from winejournal.blueprints.wines.forms import \
    NewWineForm, EditWineForm, DeleteWineForm
from winejournal.blueprints.categories.sorted_list import \
    get_sorted_categories
from winejournal.blueprints.regions.sorted_list import \
    get_sorted_regions
from winejournal.data_models.wines import Wine
from winejournal.data_models.models import engine

# setup database connection & initialize session
DBSession = sessionmaker(bind=engine)
session = DBSession()

wines = Blueprint('wines', __name__, template_folder='templates',
                       url_prefix='/wine')


@wines.route('/', methods=['GET'])
def list_wines():
    wine_list = session.query(Wine).all()
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
        print(categoryId)
        wine = Wine(
            name=new_wine_form.name.data,
            maker=new_wine_form.maker.data,
            vintage=new_wine_form.vintage.data,
            price=new_wine_form.price.data,
            description=new_wine_form.description.data,
            category=categoryId,
            region=regionId
        )

        session.add(wine)
        session.commit()
        message = 'You added {} to the journal'.format(wine.name)
        flash(message)
        return redirect(url_for('wines.list_wines'))

    return render_template('wines/wine-new.html',
                           form=new_wine_form,
                           cat_list=cat_list,
                           reg_list=reg_list)


@wines.route('/<int:wine_id>/', methods=['GET'])
def wine_detail(wine_id):
    cat_list = get_sorted_categories()
    wine = session.query(Wine).filter_by(id=wine_id).one()
    data = Prepopulated_Data(wine, cat_list)
    return render_template('wines/wine-detail.html', wine=data)


@wines.route('/<int:wine_id>/edit', methods=['GET', 'POST'])
def wine_edit(wine_id):
    cat_list = get_sorted_categories()
    wine = session.query(Wine).filter_by(id=wine_id).one()
    parent_id = wine.parent_id
    prepopulated_data = Prepopulated_Data(wine, cat_list)

    edit_wine_form = EditWineForm(obj=prepopulated_data)

    if request.method == 'POST':
        if edit_wine_form.validate_on_submit():
            parentId = get_parent_id(edit_wine_form, cat_list)

            wine.name = edit_wine_form.name.data
            wine.description = edit_wine_form.description.data
            wine.parent_id = parentId

            session.add(wine)
            session.commit()
            message = 'You updated the {} wine'.format(wine.name)
            flash(message)
            return redirect(url_for('wines.list_wines'))

    if request.method == 'DELETE':
        session.delete(wine)
        session.commit()
        message = 'You deleted the {} wine'.format(wine.name)
        flash(message)
        return redirect(url_for('wines.list_wines'))

    return render_template('wines/wine-edit.html',
                           form=edit_wine_form,
                           cat_list=cat_list,
                           parent_id=parent_id,
                           wine=wine)


@wines.route('/<int:wine_id>/delete', methods=['GET', 'POST'])
def wine_delete(wine_id):

    wine = session.query(Wine).filter_by(id=wine_id).one()
    cat_list = get_sorted_categories()
    data = Prepopulated_Data(wine, cat_list)
    delete_wine_form = DeleteWineForm(obj=wine)

    if request.method == 'POST':
        if delete_wine_form.validate_on_submit():
            session.delete(wine)
            session.commit()
            message = 'You deleted the {} wine'.format(wine.name)
            flash(message)
            return redirect(url_for('wines.list_categories'))

    return render_template('wines/wine-delete.html',
                           wine=data,
                           form=delete_wine_form)


def get_parent_id(form, cat_list):
    parentId = 0
    if form.parent.data:
        for id, name in cat_list.items():
            if name == form.parent.data:
                parentId = int(id)

    return parentId


class Prepopulated_Data:
    def __init__(self, wine, cat_list):

        self.wine = wine
        self.cat_list = cat_list
        self.name = wine.name
        self.description = wine.description
        self.parent = self.get_parent_label()

    def get_parent_label(self):
        parent_id = self.wine.parent_id
        parentLabel = ''
        if parent_id:
            for id, name in self.cat_list.items():
                if id == parent_id:
                    parentLabel = name

        return parentLabel

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