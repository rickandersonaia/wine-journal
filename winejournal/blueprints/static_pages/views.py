from flask import Blueprint, render_template, redirect, url_for, flash
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_login import current_user, login_required, login_user, logout_user
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from winejournal.data_models.users import User
from winejournal.data_models.oauth import Oauth
from winejournal.extensions import db
from winejournal.extensions import csrf, login_manager

import random, string
import httplib2
import json
import requests
from instance.settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRETS
from instance.settings import TWITTER_API_KEY, TWITTER_API_SECRET

staticPages = Blueprint('static_pages', __name__, template_folder='templates')

twitter_blueprint = make_twitter_blueprint(api_key=TWITTER_API_KEY, api_secret=TWITTER_API_SECRET)
twitter_blueprint.backend = SQLAlchemyBackend(Oauth, db.session, user=current_user, user_required=False)


@staticPages.route('/')
@login_required
def home():

    return render_template('static_pages/home.html')


@staticPages.route('/login')
def show_login():
    # state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    #                 for x in range(32))
    # login_session['state'] = state
    # return "The current login_session state is %s" % login_session['state']
    google_client_id = GOOGLE_CLIENT_ID
    # return render_template('static_pages/login.html', state=state)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@staticPages.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

    account_info = twitter.get('account/settings.json')
    account_info_json = account_info.json()

    return '<h1>Your Twitter Name is @{}</h1>'.format(account_info_json['screen_name'])


@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(blueprint, token):
    account_info = blueprint.session.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json['screen_name']
        query = db.session.query(User).filter_by(username=username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        login_user(user)


@staticPages.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
