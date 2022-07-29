import os
from flask import Flask, render_template
from utils.dep import login_manager, db
from config import config
from flask_jwt_extended import JWTManager
from utils.flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import CSRFProtect


login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
basedir = os.path.abspath(os.path.dirname(__file__))
csrf = CSRFProtect()
images = UploadSet('images', IMAGES)
docs = UploadSet('docs', ('rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'pdf'))
csrf = CSRFProtect()

jwt = JWTManager()


def create_app(config_name:str):
    """Method to initialize flask global object"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    #app.config['SQLALCHEMY_POOL_SIZE'] = 500
    #app.config['SQLALCHEMY_POOL_RECYCLE'] = 100
    #app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    #app.config['SQLALCHEMY_POOL_TIMEOUT'] = 50



    # Extension initialization
    login_manager.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    configure_uploads(app, (images))
    configure_uploads(app, docs)
    jwt.init_app(app)

    #Register url blueprints

    from blueprints.account.views import auth
    from blueprints.public.views import public


    app.register_blueprint(auth)
    app.register_blueprint(public)




    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return render_template('errors/403.html'), 403

    @app.errorhandler(403)
    def access_forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500


    return app

