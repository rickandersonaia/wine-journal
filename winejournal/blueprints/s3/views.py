"""
s3-sign.srv.py

Originally by: Mark Feltner (https://github.com/FineUploader/server-examples/tree/master/python/flask-fine-uploader-s3)
Server-side S3 upload example for Fine Uploader

Features:
* Upload to S3
* Delete from S3
* Sign Policy documents (simple uploads) and REST requests (chunked/multipart) uploads
* non-CORS environment

Enhanced by: Keiran Raine
* Converted to python3
* Added HTTPS
* More configuration via environment
* Indicate clear points for server side hooks
* Standardised access to request data for server side hooks
"""

import base64
import hashlib
import hmac
import os
import re
import sys

from flask import (Blueprint, jsonify, make_response, request, abort)
from config.settings import AWS_CLIENT_ACCESS_KEY, AWS_CLIENT_SECRET_KEY, \
    AWS_ENDPOINT, DEBUG
from winejournal.extensions import csrf

s3 = Blueprint('s3', __name__, template_folder='templates',
                    url_prefix='/s3')
