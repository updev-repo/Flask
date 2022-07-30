import functools
from datetime import datetime
from app import app
import sqlalchemy
from flask import (Blueprint, flash, get_flashed_messages, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from database import Posts, Users, db

post_bp = Blueprint('post', __name__,)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']

        msg = None

        if not name:
            flash('Username required')
        elif not password:
            flash('Username required')
        elif not email:
            flash('Username required')
        
        if msg is None:
            name = request.form['username']
            email = request.form['email']
            password = request.form['password']
            try:
                # Hash password before storage
                user = Users(name, email,  generate_password_hash(password))

                db.session.add(user)
                db.session.commit()
                flash("Your account has been created.")
            except sqlalchemy.exc.IntegrityError:
                flash(f"{name} or {email} is taken")
            else:
                return redirect(url_for('index'))
        flash(msg)
    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        msg = None 
        name = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(name=name).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['id'] = user.id
            session['name'] = name
            # Redirect to home page
            return redirect(url_for('index'))
            
        else:
            flash("Login Unsuccessful. Pleae check username and password or create an account")
        flash(msg)
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'id' not in session:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@post_bp.route('/')
def index():
    queryset = Posts.query.all()
    return render_template("index.html", posts=queryset)


@post_bp.route('/new_post', methods=['POST', 'GET'])
@login_required
def new_posts():
    name = session['name']
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user = Users.query.filter_by(name=name).first()
        user_id = user.id
        time = datetime.now()
        if not title: 
            flash('A title is required')

        posts = Posts(title, body, user_id, time)
        db.session.add(posts)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('new_posts.html')


@post_bp.route('/update_post/<int:post_id>/', methods=('GET', 'POST'))
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        
        if not title:
            flash('Title is required')
        else:
            post.title = title
            post.body = body
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_posts.html', post=post)


@post_bp.route('/delete_post/<int:post_id>/', methods=('POST',))
@login_required
def delete(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted")
    return redirect(url_for('index'))


