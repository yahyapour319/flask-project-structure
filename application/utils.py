import hashlib
import json
import os
import random
from datetime import datetime

from flask import current_app, jsonify, Response

from application.extensions import db, redis_client

'''
    contains public methods
'''


def cache_sth_in_redis(user_id):
    timeout = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    redis_client.set(key, value, timeout)


def get_from_redis(key):
    value = redis_client.get(key)
    if value:
        return value, int(redis_client.pttl(key)/1000)
    else:
        return None, 0


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['IMAGE_ALLOWED_EXTENSIONS']


