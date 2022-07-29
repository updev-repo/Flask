import os
import requests
import logging
from threading import Thread
from flask import current_app
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import render_template
from flask_mail import Message
from flask_mail import Mail
from main import create_app

# from app import mail
mail = Mail()
basedir = os.path.abspath(os.path.dirname(__file__))



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(recipient, subject, template, body):
    app = current_app()
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') or 'smtp.sendgrid.net'
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT') or 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['SSL_DISABLE'] = os.environ.get('SSL_DISABLE') or False
    app.config['MAIL_AUTH_TYPE'] = 'mailgun'
    app.config['MAILGUN_KEY'] = '5cc22bbbb7cadf0b485f49f929059725-45f7aa85-9b0bbbe9'
    app.config['MAIL_USERNAME'] = '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'
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@networked.ng'
    # app.config['MAIL_DEFAULT_SENDER_NAME'] = os.environ.get('MAIL_DEFAULT_SENDER_NAME') or 'Networked'
    # app.config['EMAIL_SENDER'] = app.config['MAIL_DEFAULT_SENDER']
    app.config['MAIL_SUPPRESS_SEND'] = False
    mail.init_app(app)
    with app.app_context():
        if app.config['MAIL_AUTH_TYPE'] == 'mailgun':
            kwargs = body
            data = {
                "from": app.config['MAIL_DEFAULT_SENDER'],
                "to": recipient,
                "subject": subject,
                "html": render_template(template + '.html', **kwargs),
                "text": (kwargs)}
            try:
                r = requests.post("https://api.mailgun.net/v3/mg.networked.com.ng/messages",
                                  auth=("api", app.config['MAILGUN_KEY']),
                                  data=data)
                print(r.status_code)
                return r
            except Exception as e:
                print(e)

        else:
            from_email = app.config['MAIL_DEFAULT_SENDER'],
            msg = Message(subject, sender=from_email, recipients=recipient)
            msg.body = body
            msg.html = template
            Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_error_message():
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Networked Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
            if app.config['LOG_TO_STDOUT']:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.INFO)
                app.logger.addHandler(stream_handler)
            else:
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/networked',
                                                   maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s '
                    '[in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Networked startup')
