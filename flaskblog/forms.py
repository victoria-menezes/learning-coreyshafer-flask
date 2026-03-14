from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import User

class RegistrationForm(FlaskForm):
    # fields
    username = StringField(
        'Username',
        validators = [
            DataRequired(), # cannot be blank
            Length(min = 2, max = 20) # cannot be over 50 characters or under 2
            ]
        )
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators = [
            DataRequired()
        ]
    )
    password_confirm = PasswordField(
        'Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )

    # submit button
    submit = SubmitField('Sign Up')

    # custom validation to prevent duplicate users
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        
        # if there is such a user:
        if user:
            raise ValidationError('Username already in use')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        
        # if there is such a user:
        if user:
            raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
    # fields
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators = [
            DataRequired()
        ]
    )

    remember = BooleanField(
        'Remember Me'
    )

    # submit button
    submit = SubmitField('Login')

