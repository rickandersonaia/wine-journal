from flask import Blueprint, render_template, redirect, url_for, \
    flash
from sqlalchemy.orm import sessionmaker

from winejournal.blueprints.categories.forms import NewCategoryForm
from winejournal.blueprints.categories.sorted_list import \
    get_toplevel_categories
from winejournal.data_models.categories import Category
from winejournal.data_models.models import engine

# setup database connection & initialize session
DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = Blueprint('categories', __name__, template_folder='templates',
                       url_prefix='/categories')


@categories.route('/', methods=['GET'])
def list_categories():
    category_list = session.query(Category).all()
    return render_template('categories/category-list.html',
                           category_list=category_list)


@categories.route('/new', methods=['GET', 'POST'])
def new_category():
    cat_list = get_toplevel_categories()
    print(cat_list)
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
            parent_id=parentId
        )

        session.add(category)
        session.commit()
        message = 'You added the {} category'.format(category.name)
        flash(message)
        return redirect(url_for('/'))

    return render_template('categories/category-new.html',
                           form=new_category_form,
                           cat_list=cat_list)


@categories.route('/<int:category_id>/', methods=['GET'])
def category_detail(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('categories/category-detail.html', category=category)
