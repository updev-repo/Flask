import json
from time import time
from enum import Enum
from utils.dep import db, login_manager, redis_q
from flask import current_app, url_for
from flask_login import UserMixin
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property



class Permission(str, Enum):
    GENERAL = 'GENERAL'
    ADMINISTER = 'ADMINISTRATOR'
    MARKETERS = 'PROMOTER'
    EDITOR = 'EDITOR'
    CUSTOMERCARE = 'CUSTOMERCARE'


class Role(db.Model):
    """Maps User roles to table for access control"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    access_role = db.Column(db.String(70), unique=True)

    @staticmethod
    def insert_roles():
        """Creates default roles, should be called once"""
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Promoter': (Permission.MARKETERS, 'marketer', False),
            'Editor': (Permission.EDITOR, 'editor', False),
            'CustomerCare': (Permission.CUSTOMERCARE, 'customercare', False),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.access_role = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
            db.session.commit()
            print('done')

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


class User(db.Model, UserMixin):
    """Maps a User object to table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True,
                   index=True, primary_key=True)
    first_name = db.Column(db.String(40))
    gender = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True, index=True)
    phone_number = db.Column(db.BigInteger, unique=True, index=True)
    last_name = db.Column(db.String(40))
    role_id = db.Column(db.Integer, db.ForeignKey(
        'roles.id', ondelete="CASCADE"))
    confirmed = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(300))
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')
    photos = db.relationship('Photo', backref='user',
                             lazy='dynamic')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if self.role is None:
                if self.email == current_app.config['ADMIN_EMAIL']:
                    self.role = Role.query.filter_by(
                        permissions=Permission.ADMINISTER).first()
                if self.role is None:
                    self.role = Role.query.filter_by(default=True).first()

            setattr(self, attribute, value)
    
    @hybrid_property
    def full_name(self):
        """Returns a user full name"""
        return self.first_name + " " + self.last_name        

    def can(self, access):
        """General method to check if a user passes an access criteria"""
        return (self.role is not None and self.role.access_role == access or 
            self.role.access_role == Permission.ADMINISTER)

    @property
    def password(self):
        """Property to hold an abstract user password"""
        if self.password_hash is None:
            raise AttributeError('`password` is not a readable attribute')
        return self.password_hash

    @password.setter
    def password(self, password):
        """Sets a user password after hashing"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password:str, *args):
        """Checks user password"""
        return check_password_hash(self.password_hash, password)
    
    def get_photo(self):
        """Returns a user profile photo"""
        image = Photo.query.filter(Photo.user_id == self.id).first()
        if image is not None:
            return url_for('_uploads.uploaded_file', setname='images',
                           filename=image.image_filename, _external=True)
        else:
            if self.gender == 'Female':
                return "https://1.semantic-ui.com/images/avatar/large/veronika.jpg"
            else:
                return "https://1.semantic-ui.com/images/avatar/large/jenny.jpg"

    def generate_email_confirmation_token(self):
        """Serializes user email confirmation token based on site secret key"""
        s = Serializer(current_app.config['SECRET_KEY'])
        return str(s.dumps({'confirm': self.email}))

    def generate_email_change_token(self, new_email):
        """Serializes user change email token based on site secret key"""
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'change_email': self.email, 'new_email': new_email})

    def generate_password_reset_token(self):
        """Serializes user password reset token based on site secret key"""
        s = Serializer(current_app.config['SECRET_KEY'])
        return str(s.dumps({'reset': self.email}))

    def confirm_account(self, token:str):
        """Checks user supplied confirmation token for validity"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=604800)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.email:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token):
        """Checks user supplied email change token for validity"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=604800)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.email:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password):
        """Checks user supplied password reset token for validity"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=604800)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.email:
            return False
        self.password_hash = generate_password_hash(new_password)
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def generate_fake(count=100, **kwargs):
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()
        roles = Role.query.all()
        if len(roles) <= 0:
            Role.insert_roles()
            roles = Role.query.all()

        seed()
        for i in range(count):
            u = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                profession=fake.job(),
                city=fake.city(),
                zip=fake.postcode(),
                state=fake.state(),
                summary_text=fake.text(),
                password='password',
                confirmed=True,
                role=choice(roles),
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def add_notification(self, name, data, related_id, permanent=False):
        """Adds user specific notification to and sends an email to user"""
        from app.utils.email import send_email
        n = Notification(name=name, payload_json=data, user=self, related_id=related_id)
        db.session.add(n)
        db.session.commit()
        n = Notification.query.get(n.id)

        body = {
            'user': self.id,
            'link': url_for('main.notifications', _external=True),
            'notification': n
        }
        redis_q.enqueue(
            send_email,
            recipient=self.email,
            subject='A new notification awaits you',
            template='account/email/notification',
            body=body
        )

        return n

    def __repr__(self):
        """Represents a string version of this object"""
        return str(self.username)


@login_manager.request_loader
def request_loader(request):
    """Flask login request loader callback method"""
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    return user if user else None


@login_manager.user_loader
def load_user(user_id: int):
    """Flask login lookup method """
    return User.query.get(int(user_id))


class Photo(db.Model):
    """Represents user, course specific photos"""
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        User.id, ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Notification(db.Model):
    """Represents user specific notifications"""
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"))
    related_id = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def get_data(self):
        return json.loads(str(self.payload_json))

    def parsed(self):
        user = User.query.filter_by(id=self.related_id).first()


class ContactMessage(db.Model):
    """Represent contact messages posted"""
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    name = db.Column(db.String(), default=None, nullable=True)
    email = db.Column(db.String(64), default=None, nullable=True)
    text = db.Column(db.Text)
    user = db.relationship("User")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
