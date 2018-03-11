from flask import Blueprint, render_template

staticPages = Blueprint('static_pages', __name__, template_folder='templates')


@staticPages.route('/')
def home():
    return render_template('static_pages/home.html')
