import boto3, os, os.path, time
from flask import Blueprint
from werkzeug.utils import secure_filename

from instance.settings import AWS_CLIENT_SECRET_KEY, \
    AWS_CLIENT_ACCESS_KEY, AWS_DEST_BUCKET, AWS_ENDPOINT, STATIC_IMAGE_PATH
from winejournal.extensions import csrf

s3 = Blueprint('s3', __name__, template_folder='templates',
               url_prefix='/s3')

s3obj = boto3.client(
    "s3",
    aws_access_key_id=AWS_CLIENT_ACCESS_KEY,
    aws_secret_access_key=AWS_CLIENT_SECRET_KEY
)


def get_filename(file):
    if file:
        return secure_filename(file.filename)
    else:
        return None


@s3.route('/upload', methods=['POST'])
@csrf.exempt
def upload_image(file):
    if file:
        filename = os.path.join(STATIC_IMAGE_PATH, file)
        with open(filename, 'rb') as data:
            try:
                s3obj.upload_fileobj(
                    data,
                    'diywptv.winejournal',
                    file,
                    ExtraArgs={
                        "ACL": "public-read"
                    }
                )
                delete_local_image(filename)
                return AWS_ENDPOINT + '/' + file

            except Exception as e:
                # This is a catch all exception, edit this part to fit your needs.
                print("Something Happened: ", e)
                return e
    else:
        return None

@s3.route('/delete-local', methods=['POST'])
@csrf.exempt
def delete_local_image(filename):
    if filename:
        os.remove(filename)




@s3.route('/delete', methods=['POST'])
@csrf.exempt
def delete_image(file):
    if file:
        filename = os.path.join(STATIC_IMAGE_PATH, file)
        with open(filename, 'rb') as data:
            try:
                s3obj.upload_fileobj(
                    data,
                    'diywptv.winejournal',
                    file,
                    ExtraArgs={
                        "ACL": "public-read"
                    }
                )
                return AWS_ENDPOINT + '/' + file

            except Exception as e:
                # This is a catch all exception, edit this part to fit your needs.
                print("Something Happened: ", e)
                return e
    else:
        return None