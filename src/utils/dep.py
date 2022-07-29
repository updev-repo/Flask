import os
import hashlib
import binascii
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from flask import request, url_for
from rq import Queue
from config import Config
# Twilio variables

db = SQLAlchemy()

login_manager = LoginManager()
basedir = os.path.abspath(os.path.dirname(__file__))

redis_conn = Redis(host=Config.RQ_DEFAULT_HOST, port=Config.RQ_DEFAULT_PORT, db=0, password=Config.RQ_DEFAULT_PASSWORD)
redis_q = Queue('high', connection=redis_conn)

login_manager = LoginManager()

db = SQLAlchemy()


def hash_pass(password: str):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash: bytes = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                         salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return salt + pwdhash  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password



def redirect_url(default='index'):
    return request.args.get('next') or \
        request.referrer or \
        url_for(default)