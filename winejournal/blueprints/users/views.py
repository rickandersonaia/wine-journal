from flask import Blueprint, render_template, redirect, url_for, \
    flash, request
from flask_login import current_user, login_required

from winejournal.blueprints.users.forms import \
    NewUserForm, EditUserForm, DeleteUserForm
from winejournal.data_models.users import User, owner_required, admin_required
from winejournal.extensions import db

users = Blueprint('users', __name__, template_folder='templates',
                  url_prefix='/users')


@users.route('/', methods=['GET'])
@login_required
def list_users():
    is_admin = current_user.is_admin()
    user_list = db.session.query(User).all()
    return render_template('users/user-list.html',
                           user_list=user_list,
                           is_admin=is_admin)


@users.route('/new', methods=['GET', 'POST'])
@login_required
def new_user():
    new_user_form = NewUserForm()
    if new_user_form.validate_on_submit():
        user = User(
            username=new_user_form.username.data,
            email=new_user_form.email.data,
            password=new_user_form.password.data,
            first_name=new_user_form.first_name.data,
            last_name=new_user_form.last_name.data,
            display_name=new_user_form.display_name.data,
            image=new_user_form.image.data,
            role=new_user_form.role.data,
            is_enabled=new_user_form.is_enabled.data,
        )

        db.session.add(user)
        db.session.commit()
        message = 'You added {} to the journal'.format(user.display_name)
        flash(message)
        return redirect(url_for('users.list_users'))

    return render_template('users/user-new.html',
                           form=new_user_form)


@users.route('/<int:user_id>/', methods=['GET'])
@login_required
def user_detail(user_id):
    is_admin = current_user.is_admin()
    is_owner = get_is_owner(user_id)
    user = db.session.query(User).filter_by(id=user_id).one()
    display_name = choose_display_name(user_id)
    return render_template('users/user-detail.html',
                           user=user,
                           display_name=display_name,
                           is_admin=is_admin,
                           is_owner=is_owner)


@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@owner_required
def user_edit(user_id):
    is_admin = current_user.is_admin()
    user = db.session.query(User).filter_by(id=user_id).one()
    user.email2 = user.email
    user.password2 = user.password
    display_name = choose_display_name(user_id)
    edit_user_form = EditUserForm(obj=user)
    edit_user_form.populate_obj(user)
    edit_user_form.validate()

    if request.method == 'POST':
        if edit_user_form.validate_on_submit():
            user.username = edit_user_form.username.data
            user.email = edit_user_form.email.data
            user.password = edit_user_form.password.data
            user.first_name = edit_user_form.first_name.data
            user.last_name = edit_user_form.last_name.data
            display_name = edit_user_form.display_name.data
            user.image = edit_user_form.image.data
            user.role = edit_user_form.role.data
            user.is_enabled = edit_user_form.is_enabled.data

            db.session.add(user)
            db.session.commit()
            message = 'You updated {}\'s user profile'.format(display_name)
            flash(message)
            return redirect(url_for('users.list_users'))

    return render_template('users/user-edit.html',
                           form=edit_user_form,
                           display_name=display_name,
                           user=user,
                           is_admin=is_admin)


@users.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@admin_required
def user_delete(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    display_name = choose_display_name(user_id)
    delete_user_form = DeleteUserForm(obj=user)

    if request.method == 'POST':
        if delete_user_form.validate_on_submit():
            db.session.delete(user)
            db.session.commit()
            message = 'You deleted the {} user'.format(display_name)
            flash(message)
            return redirect(url_for('users.list_users'))

    return render_template('users/user-delete.html',
                           form=delete_user_form,
                           user=user,
                           display_name=display_name)


def choose_display_name(user_id):
    user = db.session.query(User).get(user_id)
    if user.display_name:
        return user.display_name
    elif user.username:
        return user.username
    elif user.email:
        return user.email
    return None


def get_is_owner(user_id):
    if current_user.id == user_id:
        return True
    else:
        return False
