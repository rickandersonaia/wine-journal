from flask import Blueprint, render_template, redirect, url_for, flash
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_login import current_user, login_required, login_user, logout_user
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from winejournal.data_models.users import User
from winejournal.data_models.oauth import Oauth
from winejournal.extensions import db
from winejournal.extensions import csrf, login_manager
import boto3
import random, string
import httplib2
import json
import requests
from instance.settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRETS
from instance.settings import TWITTER_API_KEY, TWITTER_API_SECRET
from instance.settings import FACEBOOK_OAUTH_CLIENT_ID, \
    FACEBOOK_OAUTH_CLIENT_SECRET
from instance.settings import AWS_CLIENT_ACCESS_KEY, AWS_CLIENT_SECRET_KEY
from instance.settings import STATIC_IMAGE_PATH

staticPages = Blueprint('static_pages', __name__, template_folder='templates')

twitter_blueprint = make_twitter_blueprint(
    api_key=TWITTER_API_KEY,
    api_secret=TWITTER_API_SECRET)

twitter_blueprint.backend = SQLAlchemyBackend(
    Oauth, db.session,
    user=current_user,
    user_required=False)

google_blueprint = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRETS,
    scope=['profile', 'email'])

google_blueprint.backend = SQLAlchemyBackend(
    Oauth, db.session,
    user=current_user,
    user_required=False)

facebook_blueprint = make_facebook_blueprint(
    client_id=FACEBOOK_OAUTH_CLIENT_ID,
    client_secret=FACEBOOK_OAUTH_CLIENT_SECRET,
    scope=['profile', 'email'])

facebook_blueprint.backend = SQLAlchemyBackend(
    Oauth, db.session,
    user=current_user,
    user_required=False)

client = boto3.client('s3',
                      aws_access_key_id = AWS_CLIENT_ACCESS_KEY,
                      aws_secret_access_key = AWS_CLIENT_SECRET_KEY)

@staticPages.route('/')
def home():
    print(STATIC_IMAGE_PATH)
    return render_template('static_pages/home.html')


@staticPages.route('/login')
def show_login():
    return render_template('static_pages/login.html')


@staticPages.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('static_pages.home'))


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


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
    more_info = blueprint.session.get('account/verify_credentials.json')

    if account_info.ok:
        account_info_json = account_info.json()
        more_info_json = more_info.json()
        username = account_info_json['screen_name']
        image = more_info_json['profile_image_url_https']
        display_name = more_info_json['name']

        query = db.session.query(User).filter_by(username=username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(
                username=username,
                image=image,
                display_name=display_name
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('You are now logged in via Twitter')


@staticPages.route('/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text

    return '<h1>Your Google email is @{}</h1>'.format(resp.json()['email'])


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    account_info = blueprint.session.get('/oauth2/v2/userinfo')

    if account_info.ok:
        account_info_json = account_info.json()
        print (account_info_json)
        email = account_info_json['email']
        query = db.session.query(User).filter_by(email=email)

        try:
            user = query.one()
        except NoResultFound:
            user = User(
                username=email,
                email=email,
                first_name=account_info_json['given_name'],
                last_name=account_info_json['family_name'],
                image=account_info_json['picture'],
                display_name=account_info_json['name'],

            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('You are now logged in via Google')


@staticPages.route('/facebook')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))

    resp = facebook.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text

    return '<h1>Your Facebook email is @{}</h1>'.format(resp.json()['email'])


@oauth_authorized.connect_via(facebook_blueprint)
def facebook_logged_in(blueprint, token):
    account_info = blueprint.session.get('/oauth2/v2/userinfo')

    if account_info.ok:
        account_info_json = account_info.json()
        print (account_info_json)
        email = account_info_json['email']
        query = db.session.query(User).filter_by(email=email)

        try:
            user = query.one()
        except NoResultFound:
            user = User(
                username=email,
                email=email,
                first_name=account_info_json['given_name'],
                last_name=account_info_json['family_name'],
                image=account_info_json['picture'],
                display_name=account_info_json['name'],

            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('You are now logged in via Facebook')



