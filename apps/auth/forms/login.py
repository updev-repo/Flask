from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, validators


class LoginForm(FlaskForm):
    email = EmailField(label="Email")
    password = PasswordField(label="Password", validators=[validators.DataRequired()])
    submit = SubmitField(label="Login")
