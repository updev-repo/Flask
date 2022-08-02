from flask import Flask
from config.db import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = "cer3435dww342daw15fy456f67434ed2ser"
    db.init_app(app)
    db.create_all(app=app)
    return app
