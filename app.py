# import the Flask class from the flask module
from flask import Flask, render_template, url_for,redirect,request, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError
)
from flask_bcrypt import Bcrypt
from flask import Blueprint

auth = Blueprint('auth', __name__)

# create the application object
app = Flask(__name__)
bcrypt=Bcrypt(app)
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1122@localhost/flask'
app.config['SECRET_KEY']='secret'
# blueprint for auth routes in our app
#from .auth import auth as auth_blueprint
app.register_blueprint(auth)
# blueprint for non-auth parts of app


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),nullable=True, unique=True)
    name = db.Column(db.String(80), nullable=True, unique=True)
    password=db.Column(db.String(80),nullable=True)

class RegisterForm(FlaskForm):
    """User Sign-up Form."""
    username = StringField(
        validators=[
            Length(min=2),
            Email(message='Enter a valid email.'),
            DataRequired()
        ], render_kw={'placeholder':'username'}
    )
    password = PasswordField(
        validators=[ InputRequired(), Length(min=2, message='Select a stronger password.'),
        ], render_kw={'placeholder':'password!'}
    )

    submit=SubmitField('register')

    def validate_username(self,username):
        existing_username=User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError('username is not available')


class LoginForm(FlaskForm):
    """User Sign-up Form."""
    username = StringField(
        validators=[
            Length(min=2),
            Email(message='Enter a valid email.'),
            DataRequired()
        ], render_kw={'placeholder':'username'}
    )
    password = PasswordField(
        validators=[ InputRequired(), Length(min=2, message='Select a stronger password.'),
        ], render_kw={'placeholder':'password'}
    )

    submit=SubmitField('login')



# use decorators to link the function to a url
@app.route('/')
def home():
    return  render_template("home.html")  # return a string

@app.route('/users', methods = ['GET', 'POST'])
def lists():
    if(request.method == 'GET'):
  
        data = [u.username for u in User.query.all()]
        return jsonify({'data': data})

@app.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(username=email).first()
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('user already exists')
            return redirect(url_for('register'))

        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=email, password=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()
        print('returning')
        return redirect(url_for('login'))
    print('returning')
    return render_template('register.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method == 'POST':
        user=User.query.filter_by(username=email).first()
        if user:
            if bcrypt.check_password_hash(user.password,  password):
                login_user(user)
                return  redirect(url_for('dashboard'))
            else:
                flash('Please check your login details and try again.')
                return  redirect(url_for('login'))
        else:
            flash('user does not exist')
            return redirect(url_for('login'))
    # if request.method == 'POST':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #         return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/dashboard',  methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/userlist', methods=['GET', 'POST'])
@login_required
def user_list():
    uss=User.query.all()
    return render_template('user_list.html',uss=uss)

# start the server with the 'run()' method
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)