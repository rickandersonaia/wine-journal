from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from sqlalchemy.orm import sessionmaker

from winejournal.blueprints.regions.forms import \
    NewCategoryForm, EditCategoryForm, DeleteCategoryForm
from winejournal.blueprints.regions.sorted_list import \
    get_toplevel_categories
from winejournal.data_models.regions import Region
from winejournal.data_models.models import engine

# setup database connection & initialize session
DBSession = sessionmaker(bind=engine)
session = DBSession()

regions = Blueprint('regions', __name__, template_folder='templates',
                       url_prefix='/regions')


@regions.route('/', methods=['GET'])
def list_categories():
    category_list = get_toplevel_categories()
    return render_template('regions/region-list.html',
                           category_list=category_list)


@regions.route('/new', methods=['GET', 'POST'])
def new_category():
    cat_list = get_toplevel_categories()
    new_category_form = NewCategoryForm()
    if new_category_form.validate_on_submit():
        parentId = 0
        if new_category_form.parent.data:
            for id, name in cat_list.items():
                if name == new_category_form.parent.data:
                    parentId = int(id)
        region = Region(
            name=new_category_form.name.data,
            description=new_category_form.description.data,
            parent_id=parentId
        )

        session.add(region)
        session.commit()
        message = 'You added the {} region'.format(region.name)
        flash(message)
        return redirect(url_for('regions.list_categories'))

    return render_template('regions/region-new.html',
                           form=new_category_form,
                           cat_list=cat_list)


@regions.route('/<int:category_id>/', methods=['GET'])
def category_detail(category_id):
    cat_list = get_toplevel_categories()
    region = session.query(Region).filter_by(id=category_id).one()
    data = Prepopulated_Data(region, cat_list)
    return render_template('regions/region-detail.html', region=data)


@regions.route('/<int:category_id>/edit', methods=['GET', 'POST'])
def category_edit(category_id):
    cat_list = get_toplevel_categories()
    region = session.query(Region).filter_by(id=category_id).one()
    parent_id = region.parent_id
    prepopulated_data = Prepopulated_Data(region, cat_list)

    edit_category_form = EditCategoryForm(obj=prepopulated_data)

    if request.method == 'POST':
        if edit_category_form.validate_on_submit():
            parentId = get_parent_id(edit_category_form, cat_list)

            region.name = edit_category_form.name.data
            region.description = edit_category_form.description.data
            region.parent_id = parentId

            session.add(region)
            session.commit()
            message = 'You updated the {} region'.format(region.name)
            flash(message)
            return redirect(url_for('regions.list_categories'))

    if request.method == 'DELETE':
        session.delete(region)
        session.commit()
        message = 'You deleted the {} region'.format(region.name)
        flash(message)
        return redirect(url_for('regions.list_categories'))

    return render_template('regions/region-edit.html',
                           form=edit_category_form,
                           cat_list=cat_list,
                           parent_id=parent_id,
                           region=region)


@regions.route('/<int:category_id>/delete', methods=['GET', 'POST'])
def category_delete(category_id):

    region = session.query(Region).filter_by(id=category_id).one()
    cat_list = get_toplevel_categories()
    data = Prepopulated_Data(region, cat_list)
    delete_category_form = DeleteCategoryForm(obj=region)

    if request.method == 'POST':
        if delete_category_form.validate_on_submit():
            session.delete(region)
            session.commit()
            message = 'You deleted the {} region'.format(region.name)
            flash(message)
            return redirect(url_for('regions.list_categories'))

    return render_template('regions/region-delete.html',
                           region=data,
                           form=delete_category_form)


def get_parent_id(form, cat_list):
    parentId = 0
    if form.parent.data:
        for id, name in cat_list.items():
            if name == form.parent.data:
                parentId = int(id)

    return parentId


class Prepopulated_Data:
    def __init__(self, region, cat_list):

        self.region = region
        self.cat_list = cat_list
        self.name = region.name
        self.description = region.description
        self.parent = self.get_parent_label()

    def get_parent_label(self):
        parent_id = self.region.parent_id
        parentLabel = ''
        if parent_id:
            for id, name in self.cat_list.items():
                if id == parent_id:
                    parentLabel = name

        return parentLabel
