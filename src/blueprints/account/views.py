import datetime

from models import *
from utils.dep import db, redis_q
from utils.email import send_email
from flask import (Blueprint, render_template, redirect,
                   request, url_for, flash, make_response)
from flask_jwt_extended import create_access_token
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .forms import *

auth = Blueprint('auth', __name__, url_prefix='/account')


@auth.route('/login', methods=["POST", "GET"])
def login():
    next = ''
    if 'next' in request.values:
        next = request.values['next']
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        # read form data
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            # Locate user
            user = User.query.filter_by(email=email).first()

            # Check the password
            if user is not None and user.verify_password(password, user.password):
                login_user(user, form.remember_me.data)
                if request.form['next'] != '':
                    resp = make_response(redirect(request.form['next']))
                    resp.set_cookie('user_token', create_access_token(
                        identity=user.email), expires=datetime.datetime.now() + datetime.timedelta(days=30))
                    return resp
                flash('You are now logged in. Welcome back!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid email or password', 'error')
    return render_template('auth/login.html', form=form, next=next)


@auth.route('/register', methods=["POST", "GET"])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                user: User = User(**request.form)
                db.session.add(user)
                db.session.commit()
                token: str = user.generate_email_confirmation_token()
                link = url_for('auth.confirm', token=token, _external=True)

                redis_q.enqueue(send_email, template="/account/email/confirm" \
                                , body={"user": user, "link": link}, subject="Confirm your account",
                                recipient=user.email)
                # get_queue().enqueue(send_sms,to_phone=(area_code) + (phone_number), message=message)
                flash(f'A confirmation link has been sent  {user.email}.', 'warning')
                return redirect(url_for('auth.unconfirmed'))
            else:
                flash('Error! Data was not added.', 'error')
    return render_template('auth/signup.html', form=form)


@auth.route("/forgot/password", methods=["GET", "POST"])
def forgot_password():
    """ Serves a forgot password form """
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data).first()
        if user:
            token = user.generate_password_reset_token()
            reset_link = url_for('auth.password_reset',
                                 token=token, _external=True)
            data = {'token': token, 'reset_link': reset_link, 'user': user}
            redis_q.enqueue(send_email, recipients=user.email, template='auth/email/reset_password', body=data,
                            subject="Change your password")
        flash('A password reset link has been sent to {}.'.format(user.email), 'warning')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)


@auth.route("/password_reset/<token>", methods=["GET", "POST"])
def password_reset(token):
    """ Users get this link via forgot-password email
        Serves a form for a password reset
    """
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data).first()
        if user is None:
            flash('Invalid email address.', 'form-error')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.new_password.data):
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('auth.login'))
        else:
            flash('The password reset link is invalid or has expired.',
                  'form-error')
            return redirect(url_for('main.index'))
    return render_template("auth/password_reset.html", form=form)


@auth.route("/confirm/<token>", methods=["GET", "POST"])
@login_required
def confirm(token: str):
    """ Users get this link via email to confirm account
        Serves a form for a password reset
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.confirm_account(token):
        flash('Your account has been confirmed successfully.', 'form-success')
        return redirect(url_for('main.index'))
    else:
        flash('Invalid Token or expired.',
              'form-error')
        return redirect(url_for('auth.unconfirmed'))




@auth.route('/manage/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    logo = SiteLogo.query.first()
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for(
                'account.change_email', token=token, _external=True)
            redis_q.enqueue(
                send_email,
                recipient=new_email,
                subject='Confirm Your New Email',
                template='account/email/change_email',
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user.id,
                change_email_link=change_email_link)
            flash('A confirmation link has been sent to {}.'.format(new_email),
                  'warning')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('auth/manage.html', form=form, logo=logo)


@auth.route('/manage/info', methods=['GET'])
@login_required
def manage():
    logo = SiteLogo.query.first()
    return render_template('auth/manage.html', user=current_user, form=None, logo=logo)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('public.index'))


@auth.route('/manage/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.password.data):
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            current_user.password_hash = hashed_password
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Original password is invalid.', 'error')
    return render_template('auth/manage.html', form=form)


@auth.route('/resend/token', methods=["GET", "POST"])
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    token: str = current_user.generate_email_confirmation_token()
    user = current_user.email
    subject = 'Confirm your account'
    body = {
        'confirm_link': url_for('auth.confirm', token=token, _external=True),
        'token': token
    }
    redis_q.enqueue(send_email, recipients=user, body=body, subject=subject, template='auth/email/confirm')
    flash('An confirmation link has been sent to {}.'.format(current_user.email), 'warning')
    return redirect(url_for('auth.unconfirmed'))




@auth.route('/unconfirmed', methods=['GET'])
@login_required
def unconfirmed():
    logo = SiteLogo.query.first()
    return render_template('auth/unconfirmed.html', user=current_user, form=None, logo=logo)


# @auth.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:8] != 'account.':
        return redirect(url_for('auth.confirm'))
