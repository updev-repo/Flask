from dataclasses import dataclass
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from config.db import db
from config.login import login_manager

salt = "CHANGE THIS LATER"


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


@dataclass
class User(db.Model, UserMixin):
    id: int
    fullname: str
    email: str

    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(32))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {"fullname": self.fullname}
