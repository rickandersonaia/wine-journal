from datetime import timedelta
import json
import os

DEBUG = True
JSDEBUG = 'true'
ASSETS_DEBUG = True

# SERVER_NAME = '0.0.0.0:5000'
# SERVER_NAME = 'https://our-wine-journal.herokuapp.com/'
SECRET_KEY = os.environ['SECRET_KEY']

#set this flag to true when an initial user has been created and is given the
# admin role.  This should be false on startup
INITIAL_ADMIN_SETUP = False

ROOT_PATH = os.path.dirname(os.path.realpath('../winejournal/app.py'))
STATIC_FOLDER_PATH = os.path.dirname(os.path.realpath('../wine-journal/winejournal/static/img/'))
STATIC_IMAGE_PATH = os.path.normcase(os.path.realpath(os.path.join('..','wine-journal', 'winejournal', 'static', 'img')))

UPLOADED_PHOTOS_DEST = 'winejournal/static/img'
UPLOADED_PHOTOS_URL = '/static/img/'
DEFAULT_CATEGORY_IMAGE = UPLOADED_PHOTOS_URL + 'generic-wine-category.jpg'
DEFAULT_REGION_IMAGE = UPLOADED_PHOTOS_URL + 'generic-wine-region.jpg'
DEFAULT_WINE_IMAGE = UPLOADED_PHOTOS_URL + 'generic-wine-bottle.jpg'

# SQLAlchemy.
# db_uri = 'postgres://mgjnxqagefnuxl:60ea9f2d1067e6c01906c26ec33b5f6921a58ab9a9e8a012ecba9560853b88d1@ec2-54-235-193-34.compute-1.amazonaws.com:5432/d549853lc81enb'
# username: winejournal
# password: devpassword
# SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)

GOOGLE_CLIENT_ID = os.environ('WJ_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRETS = os.environ('WJ_GOOGLE_CLIENT_SECRETS')
TWITTER_API_KEY = 'JpWODQRv8ACIowNruaV272d9O'
TWITTER_API_SECRET = 'zVLLl66TQphRPvdR5QaxB2Ic9dNvc9d6aRODE7p6M1HXueERlM'

FACEBOOK_OAUTH_CLIENT_ID = json.loads(
    open('winejournal/fb_client_secrets.json', 'r').read())['web']['app_id']
FACEBOOK_OAUTH_CLIENT_SECRET = json.loads(
    open('winejournal/fb_client_secrets.json', 'r').read())['web']['app_secret']



APPLICATION_NAME = "Restaurant Menu Application"

# s3 variables
AWS_CLIENT_ACCESS_KEY='AKIAICFFYHMTX2AKPKCQ'
AWS_CLIENT_SECRET_KEY='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'
AWS_DEST_BUCKET='diywptv.winejournal'
AWS_ENDPOINT='https://s3-us-west-1.amazonaws.com/diywptv.winejournal'
AWS_HOST = 's3-us-west-1.amazonaws.com'
