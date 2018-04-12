from datetime import timedelta

DEBUG = True
ASSETS_DEBUG = True

SERVER_NAME = 'localhost:5000'
SECRET_KEY = 'insecurekeyfordev'
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRETS = ''
TWITTER_API_KEY = ''
TWITTER_API_SECRET = ''

#set this flag to true when an initial user has been created and is given the
# admin role.  This should be false on startup
INITIAL_ADMIN_SETUP = True



# Flask-Mail.
# MAIL_DEFAULT_SENDER = 'contact@local.host'
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'you@gmail.com'
# MAIL_PASSWORD = 'awesomepassword'


# SQLAlchemy.
db_uri = 'postgresql+psycopg2://winejournal:devpassword@localhost:5432/winejournal'
# username: winejournal
# password: devpassword
SQLALCHEMY_DATABASE_URI = db_uri
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


