from flask import Blueprint, render_template

categories = Blueprint('categories', __name__, template_folder='templates', url_prefix='/categories')


@categories.route('/new')
def new_category():
    return render_template('categories/new-category.html')
