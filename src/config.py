import os
import sys
import datetime

# from raygun4py.middleware import flask as flask_raygun

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.parse
# else:
#  import urlparse
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = os.environ.get('APP_NAME', "UPDEV.com")

    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.sendgrid.net')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'support@FHI-360.com')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SSL_DISABLE = False
    EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX', 'FHI-360')
    MAIL_DEFAULT_SENDER_NAME = os.environ.get('MAIL_DEFAULT_SENDER_NAME', 'FHI-360')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USERNAME =os.environ.get('MAIL_USERNAME', 'apikey')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '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')
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = False
    # Analytics
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID')
    SEGMENT_API_KEY = os.environ.get('SEGMENT_API_KEY')
    RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY') or ''
    RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY') or ''
    RECAPTCHA_ENABLED = os.environ.get('RECAPTCHA_ENABLED') or True

    # Admin account
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')
    ADMIN_MOBILE_PHONE = os.environ.get('ADMIN_MOBILE_PHONE', '000000000000')
    ADMIN_AREA_CODE = '+234'
    ADMIN_EMAIL = os.environ.get(
        'ADMIN_EMAIL', 'fhi360@gmail.com')
    EMAIL_SUBJECT_PREFIX = '[{}]'.format(APP_NAME)
    EMAIL_SENDER = '{app_name} Admin <{email}>'.format(
        app_name=APP_NAME, email=MAIL_USERNAME)

    REDIS_URL = os.getenv('REDISTOGO_URL', 'http://localhost:6379')
    CKEDITOR_FILE_UPLOADER = os.environ.get('CKEDITOR_FILE_UPLOADER', 'main.upload')
    CKEDITOR_SERVE_LOCAL = os.environ.get('CKEDITOR_SERVE_LOCAL', True)
    CKEDITOR_HEIGHT = os.environ.get('CKEDITOR_HEIGHT',400)
    CKEDITOR_ENABLE_CSRF = os.environ.get('CKEDITOR_ENABLE_CSRF',  True)
    RAYGUN_APIKEY = os.environ.get('RAYGUN_APIKEY')



    # Parse the REDIS_URL to set RQ config variables
    if PYTHON_VERSION == 3:
        urllib.parse.uses_netloc.append('redis')
        url = urllib.parse.urlparse(REDIS_URL)

    RQ_DEFAULT_HOST = url.hostname
    RQ_DEFAULT_PORT = url.port
    RQ_DEFAULT_PASSWORD = url.password
    RQ_DEFAULT_DB = 0

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = datetime.timedelta(days=365)
    UPLOADED_IMAGES_DEST = '/home/ubuntu/networkedng/flask-base/app/static/photo/' if \
        not os.environ.get('UPLOADED_IMAGES_DEST') else os.path.dirname(os.path.realpath(__file__)) + os.environ.get(
        'UPLOADED_IMAGES_DEST')
    UPLOADED_DOCS_DEST = '/home/ubuntu/networkedng/flask-base/app/static/docs/' if \
        not os.environ.get('UPLOADED_DOCS_DEST') else os.path.dirname(os.path.realpath(__file__)) + os.environ.get(
        'UPLOADED_DOCS_DEST')
    docs = UPLOADED_DOCS_DEST
    UPLOADED_PATH = os.path.join(basedir, 'uploads')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', "postgresql://postgres:postgres@localhost/fhi_360")

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', "postgresql://postgres:Prod_db_Networked_@__21@localhost:5433/networked")    
    SSL_DISABLE = (os.environ.get('SSL_DISABLE') or 'True') == 'True'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY', 'SECRET_KEY IS NOT SET')


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'unix': UnixConfig
}
