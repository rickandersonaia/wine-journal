import json
import os
import os.path

import boto3
from flask import Blueprint, request
from werkzeug.utils import secure_filename

from config.settings import TEMP_IMAGE_PATH, STATIC_IMAGE_PATH, AWS_ENDPOINT, \
    AWS_DEST_BUCKET, AWS_REGION
from instance.settings import AWS_CLIENT_SECRET_KEY, AWS_CLIENT_ACCESS_KEY
from winejournal.extensions import csrf

s3 = Blueprint('s3', __name__, template_folder='templates',
               url_prefix='/s3')

s3obj = boto3.client(
    "s3",
    aws_access_key_id=AWS_CLIENT_ACCESS_KEY,
    aws_secret_access_key=AWS_CLIENT_SECRET_KEY,
    region_name=AWS_REGION
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
        filename = os.path.join(TEMP_IMAGE_PATH, file)
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
                # This is a catch all exception.
                print("Something Happened: ", e)
                return e
    else:
        return None


@s3.route('/delete-local', methods=['POST'])
@csrf.exempt
def delete_local_image(filename):
    if filename:
        os.remove(filename)


"""
This is intended to delete an unused image from Amazon S3.  However it is not
currently used and needs to be reworked
"""


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
                # This is a catch all exception.
                print("Something Happened: ", e)
                return e
    else:
        return None


"""
This was suggested by Heroku as a way of creating a signing request and then passing
it back to a javascript client.  It is retained here for future reference
"""


@s3.route('/sign-s3')
@csrf.exempt
def sign_s3():
    # Load required data from the request
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    # Initialise the S3 client
    s3obj = boto3.client(
        "s3",
        aws_access_key_id=AWS_CLIENT_ACCESS_KEY,
        aws_secret_access_key=AWS_CLIENT_SECRET_KEY,
        region_name=AWS_REGION
    )

    # Generate and return the presigned URL
    presigned_post = s3obj.generate_presigned_post(
        Bucket=AWS_DEST_BUCKET,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    # Return the data to the client
    return json.dumps({
        'data': presigned_post,
        'url': 'https://s3-us-west-1.amazonaws.com/%s/%s' % (
            AWS_DEST_BUCKET, file_name)
    })
