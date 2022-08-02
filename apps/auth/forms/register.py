from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators


class RegisterForm(FlaskForm):
    fullname = StringField(label="Fullname", validators=[validators.DataRequired()])
    password = PasswordField(label="Password", validators=[validators.DataRequired()])
    email = EmailField(label="Email", validators=[validators.DataRequired()])
    submit = SubmitField(label="Register")
