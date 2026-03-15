from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
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

class UpdateAccountForm(FlaskForm):
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
    picture = FileField(
        'Update profile picture',
        validators=[
            FileAllowed(
                ['png', 'jpg', 'jpeg']
            )
        ]
    )

    # submit button
    submit = SubmitField('Update')

    # custom validation to prevent duplicate users
    def validate_username(self, username):
        # if its changed
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            
            # if there is such a user:
            if user:
                raise ValidationError('Username already in use')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            
            # if there is such a user:
            if user:
                raise ValidationError('Email already in use')

class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired()
        ]
    )

    content = TextAreaField(
        'Content',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        'Post'
    )

class RequestResetForm(FlaskForm):
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField(
        'Request Password Reset'
    )

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        
        # if there is not such a user:
        if user is None:
            # raise ValidationError('There is no account with that email') # bad security
            return

class ResetPasswordForm(FlaskForm):
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

    submit = SubmitField(
        'Reset Password'
    )