from flask import Blueprint, render_template, flash, url_for
from werkzeug.utils import redirect

from apps.auth.forms.login import LoginForm
from apps.auth.forms.register import RegisterForm
from apps.auth.model.user import User
from config.db import db
from flask_login import login_user, logout_user

auth = Blueprint("auth", __name__, template_folder="./templates", static_url_path="/static/auth",
                 static_folder="./static")


@auth.route("/login")
@auth.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = ""
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            error = "user does not exist"
        elif user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("account.account_page"))
        else:
            error = "password is incorrect"
    return render_template("login.html", form=form, error=error)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    error = ""
    if form.validate_on_submit():
        user_in_db = User.query.filter_by(email=form.email.data).first()
        if user_in_db:
            error = "user already exist"
        else:
            user = User(fullname=form.fullname.data, password=form.password.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("account.account_page"))
    return render_template("register.html", form=form, error=error)


@auth.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("auth.login"))
