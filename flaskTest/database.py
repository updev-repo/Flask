from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, null
from app import app

app.secret_key = "default"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/flaskauth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True)
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500))
    posts = db.relationship('Posts', backref='post_author', lazy=True)


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(500))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, body, user_id, time):
        self.title = title 
        self.body = body 
        self.user_id = user_id
        self.time = time
