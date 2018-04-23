import json
import os

# SERVER_NAME = '0.0.0.0:5000'
# SERVER_NAME = 'https://our-wine-journal.herokuapp.com/'
SECRET_KEY = os.environ['SECRET_KEY']

# SQLAlchemy.
# db_uri = 'postgres://mgjnxqagefnuxl:60ea9f2d1067e6c01906c26ec33b5f6921a58ab9a9e8a012ecba9560853b88d1@ec2-54-235-193-34.compute-1.amazonaws.com:5432/d549853lc81enb'
# username: winejournal
# password: devpassword
# SQLALCHEMY_DATABASE_URI = db_uri
DB_PASSWORD = os.environ[
    'WINEJOURNAL_DB_PASSWORD']  # 60ea9f2d1067e6c01906c26ec33b5f6921a58ab9a9e8a012ecba9560853b88d1
DB_HOST = os.environ[
    'WINEJOURNAL_DB_HOST']  # ec2-54-235-193-34.compute-1.amazonaws.com
DATABASE_NAME = os.environ['WINEJOURNAL_DATABASE_NAME']  # d549853lc81enb
SQLALCHEMY_TRACK_MODIFICATIONS = False

GOOGLE_CLIENT_ID = os.environ['WJ_GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRETS = os.environ['WJ_GOOGLE_CLIENT_SECRETS']
TWITTER_API_KEY = 'JpWODQRv8ACIowNruaV272d9O'
TWITTER_API_SECRET = 'zVLLl66TQphRPvdR5QaxB2Ic9dNvc9d6aRODE7p6M1HXueERlM'

FACEBOOK_OAUTH_CLIENT_ID = json.loads(
    open('winejournal/fb_client_secrets.json', 'r').read())['web']['app_id']
FACEBOOK_OAUTH_CLIENT_SECRET = json.loads(
    open('winejournal/fb_client_secrets.json', 'r').read())['web']['app_secret']

# s3 variables
AWS_CLIENT_ACCESS_KEY = 'AKIAIWLPMGZLEIUCA3HA'
AWS_CLIENT_SECRET_KEY = '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'
AWS_DEST_BUCKET = 'diywptv.winejournal'
AWS_ENDPOINT = 'https://s3-us-west-1.amazonaws.com/diywptv.winejournal'
AWS_HOST = 's3-us-west-1.amazonaws.com'
AWS_REGION = 'us-west-1'
