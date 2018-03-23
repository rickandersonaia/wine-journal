from flask import Blueprint, render_template, request, redirect, url_for, \
    flash, jsonify
from winejournal.data_models.categories import Category
from winejournal.data_models.models import engine, Base
from winejournal.blueprints.categories.forms import NewCategoryForm
from sqlalchemy.orm import sessionmaker

#setup database connection & initialize session
DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = Blueprint('categories', __name__, template_folder='templates', url_prefix='/categories')

@categories.route('/', methods=['GET'])
def list_categories():
    category_list = session.query(Category).all()
    return render_template('categories/list-categories.html', category_list=category_list)


@categories.route('/new', methods=['GET', 'POST'])
def new_category():
    new_category_form = NewCategoryForm()
    if new_category_form.validate_on_submit():
        category = Category(
            name=new_category_form.name.data,
            description=new_category_form.description.data,
            parent_id=0
        )

        session.add(category)
        session.commit()
        message = 'You added the {} category'.format(category.name)
        flash(message)
        return redirect(url_for('/'))

    return render_template('categories/new-category.html', form=new_category_form)

