"""Form classes."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class RegistrationForm(FlaskForm):
    """Registration form."""

    username = StringField(label='username_label', validators=[
        DataRequired(message="Username required"),
        Length(min=3, max=25, message="Username must be between 4 and 25 characters")])

    email = EmailField(label='email_label', validators=[
        DataRequired("Email required"),
        Email("Email must be valid")
    ])

    password = PasswordField(label='password_label', validators=[
        DataRequired(message="Password required"),
        Length(min=4, max=25, message="Password must be between 4 and 25 characters")])

    confirm_pswd = PasswordField(label='confirm_pswd_label', validators=[
        DataRequired(message="Must confirm password"),
        EqualTo('password', message='Passwords must match')])

    submit_button = SubmitField('Create')


class LoginForm(FlaskForm):
    """Login form."""

    email = EmailField(label='email', validators=[
        DataRequired("Email required"),
        Email("Valid email required")
    ])

    password = PasswordField(label='password', validators=[
        DataRequired("Password required")
    ])

    submit_button = SubmitField("Login")
