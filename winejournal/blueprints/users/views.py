from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from flask_login import current_user, login_required

from winejournal.blueprints.users.forms import \
    NewUserForm, EditUserForm, DeleteUserForm
from winejournal.data_models.users import User
from winejournal.extensions import db

users = Blueprint('users', __name__, template_folder='templates',
                  url_prefix='/users')


@users.route('/', methods=['GET'])
@login_required
def list_users():
    current_user
    user_list = db.session.query(User).all()
    return render_template('users/user-list.html',
                           user_list=user_list)


@users.route('/new', methods=['GET', 'POST'])
@login_required
def new_user():
    new_user_form = NewUserForm()
    if new_user_form.validate_on_submit():
        user = User(
            name=new_user_form.name.data,
            maker=new_user_form.maker.data,
            vintage=new_user_form.vintage.data,
            price=new_user_form.price.data,
            description=new_user_form.description.data,
        )

        db.session.add(user)
        db.session.commit()
        message = 'You added {} to the journal'.format(user.name)
        flash(message)
        return redirect(url_for('users.list_users'))

    return render_template('users/user-new.html',
                           form=new_user_form)


@users.route('/<int:user_id>/', methods=['GET'])
@login_required
def user_detail(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    return render_template('users/user-detail.html', user=user)


@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()

    edit_user_form = EditUserForm(obj=user)

    if request.method == 'POST':
        if edit_user_form.validate_on_submit():
            user.name = edit_user_form.name.data
            user.maker = edit_user_form.maker.data
            user.vintage = edit_user_form.vintage.data
            user.price = edit_user_form.price.data
            user.description = edit_user_form.description.data
            user.owner = edit_user_form.owner.data

            db.session.add(user)
            db.session.commit()
            message = 'You updated the {} user'.format(user.name)
            flash(message)
            return redirect(url_for('users.list_users'))

    return render_template('users/user-edit.html', user=user)


@users.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def user_delete(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    delete_user_form = DeleteUserForm(obj=user)

    if request.method == 'POST':
        if delete_user_form.validate_on_submit():
            db.session.delete(user)
            db.session.commit()
            message = 'You deleted the {} user'.format(user.name)
            flash(message)
            return redirect(url_for('users.list_users'))

    return render_template('users/user-delete.html',
                           form=delete_user_form,
                           user=user)
