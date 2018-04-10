from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from flask_login import current_user, login_required
from winejournal.blueprints.categories.forms import \
    NewCategoryForm, EditCategoryForm, DeleteCategoryForm
from winejournal.blueprints.categories.sorted_list import \
    get_sorted_categories
from winejournal.data_models.categories import Category, category_owner_required
from winejournal.data_models.users import admin_required
from winejournal.extensions import db

categories = Blueprint('categories', __name__, template_folder='templates',
                       url_prefix='/categories')


@categories.route('/', methods=['GET'])
def list_categories():
    category_list = get_sorted_categories()
    return render_template('categories/category-list.html',
                           category_list=category_list)


@categories.route('/new', methods=['GET', 'POST'])
def new_category():
    cat_list = get_sorted_categories()
    new_category_form = NewCategoryForm()
    if new_category_form.validate_on_submit():
        parentId = 0
        if new_category_form.parent.data:
            for id, name in cat_list.items():
                if name == new_category_form.parent.data:
                    parentId = int(id)
        category = Category(
            name=new_category_form.name.data,
            description=new_category_form.description.data,
            parent_id=parentId,
            owner = current_user.id
        )

        db.session.add(category)
        db.session.commit()
        message = 'You added the {} category'.format(category.name)
        flash(message)
        return redirect(url_for('categories.list_categories'))

    return render_template('categories/category-new.html',
                           form=new_category_form,
                           cat_list=cat_list)


@categories.route('/<int:category_id>/', methods=['GET'])
def category_detail(category_id):
    is_admin = current_user.is_admin()
    is_owner = get_is_owner(category_id)
    cat_list = get_sorted_categories()
    category = db.session.query(Category).filter_by(id=category_id).one()
    data = Prepopulated_Data(category, cat_list)
    return render_template('categories/category-detail.html',
                           category=data,
                           is_admin=is_admin,
                           is_owner=is_owner)


@categories.route('/<int:category_id>/edit', methods=['GET', 'POST'])
@category_owner_required
def category_edit(category_id):
    is_admin = current_user.is_admin()
    is_owner = get_is_owner(category_id)
    cat_list = get_sorted_categories()
    category = db.session.query(Category).filter_by(id=category_id).one()
    parent_id = category.parent_id
    prepopulated_data = Prepopulated_Data(category, cat_list)

    edit_category_form = EditCategoryForm(obj=prepopulated_data)

    if request.method == 'POST':
        if edit_category_form.validate_on_submit():
            parentId = get_parent_id(edit_category_form, cat_list)

            category.name = edit_category_form.name.data
            category.description = edit_category_form.description.data
            category.parent_id = parentId

            db.session.add(category)
            db.session.commit()
            message = 'You updated the {} category'.format(category.name)
            flash(message)
            return redirect(url_for('categories.list_categories'))


    return render_template('categories/category-edit.html',
                           form=edit_category_form,
                           cat_list=cat_list,
                           parent_id=parent_id,
                           category=category,
                           is_admin=is_admin,
                           is_owner=is_owner)


@categories.route('/<int:category_id>/delete', methods=['GET', 'POST'])
@admin_required
def category_delete(category_id):
    category = db.session.query(Category).filter_by(id=category_id).one()
    cat_list = get_sorted_categories()
    data = Prepopulated_Data(category, cat_list)
    delete_category_form = DeleteCategoryForm(obj=category)

    if request.method == 'POST':
        if delete_category_form.validate_on_submit():
            db.session.delete(category)
            db.session.commit()
            message = 'You deleted the {} category'.format(category.name)
            flash(message)
            return redirect(url_for('categories.list_categories'))

    return render_template('categories/category-delete.html',
                           category=data,
                           form=delete_category_form)


def get_parent_id(form, cat_list):
    parentId = 0
    if form.parent.data:
        for id, name in cat_list.items():
            if name == form.parent.data:
                parentId = int(id)

    return parentId


class Prepopulated_Data:
    def __init__(self, category, cat_list):

        self.category = category
        self.cat_list = cat_list
        self.name = category.name
        self.description = category.description
        self.parent = self.get_parent_label()

    def get_parent_label(self):
        parent_id = self.category.parent_id
        parentLabel = ''
        if parent_id:
            for id, name in self.cat_list.items():
                if id == parent_id:
                    parentLabel = name

        return parentLabel


def get_is_owner(category_id):
    cat = db.session.query(Category).get(category_id)
    if cat.owner == current_user.id:
        return True
    else:
        return False

