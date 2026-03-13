from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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

