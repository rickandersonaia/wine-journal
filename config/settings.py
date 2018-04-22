from datetime import timedelta
import os

DEBUG = True
ASSETS_DEBUG = True

# SERVER_NAME = '0.0.0.0:5000'
SECRET_KEY = os.environ['SECRET_KEY']

# Social site login authentication
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRETS = ''
TWITTER_API_KEY = ''
TWITTER_API_SECRET = ''
FACEBOOK_OAUTH_CLIENT_ID = ''
FACEBOOK_OAUTH_CLIENT_SECRET = ''

#set this flag to true when an initial user has been created and is given the
# admin role.  This should be false on startup
INITIAL_ADMIN_SETUP = False

UPLOADED_PHOTOS_DEST = 'winejournal/static/img'
UPLOADED_PHOTOS_URL = '/static/img/'
DEFAULT_CATEGORY_IMAGE = '/static/img/generic-wine-category.jpg'
DEFAULT_REGION_IMAGE = '/static/img/generic-wine-region.jpg'
DEFAULT_WINE_IMAGE = '/static/img/generic-wine-bottle.jpg'

# SQLAlchemy.
# DB_URI = 'postgres://mgjnxqagefnuxl:60ea9f2d1067e6c01906c26ec33b5f6921a58ab9a9e8a012ecba9560853b88d1@ec2-54-235-193-34.compute-1.amazonaws.com:5432/d549853lc81enb'
# DB_URI = 'postgresql+psycopg2://winejournal:devpassword@localhost:5432/winejournal'
# username: winejournal
# password: devpassword
DB_USERNAME=os.environ['WINEJOURNAL_DB_USERNAME'] #mgjnxqagefnuxl
DB_PASSWORD=os.environ['WINEJOURNAL_DB_PASSWORD'] #60ea9f2d1067e6c01906c26ec33b5f6921a58ab9a9e8a012ecba9560853b88d1
DB_HOST=os.environ['WINEJOURNAL_DB_HOST'] #ec2-54-235-193-34.compute-1.amazonaws.com
DATABASE_NAME=os.environ['WINEJOURNAL_DATABASE_NAME'] #d549853lc81enb
DB_URI = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)

OAUTHLIB_INSECURE_TRANSPORT=1
OAUTHLIB_RELAX_TOKEN_SCOPE=1


# s3 variables
AWS_CLIENT_ACCESS_KEY=''
AWS_CLIENT_SECRET_KEY=''
AWS_DEST_BUCKET='winejournal'
AWS_ENDPOINT='https://s3-us-west-2.amazonaws.com/winejournal'
AWS_HOST = 's3-us-west-2.amazonaws.com'


