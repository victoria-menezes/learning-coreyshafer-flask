from flask import Blueprint

from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, db, bcrypt
from flaskblog.users.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm,
    RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post

from flask_login import login_user, current_user, logout_user, login_required

import os
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint(
    'users', # name
    __name__
)

@users.route('/register',
           methods=['GET', 'POST'] # accepts get and post requests
           )
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit(): # if form submitted was valid
        # hashing password
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = hashed
            )
        
        db.session.add(user)
        db.session.commit()

        flash(f'You account has been created, you may now log in',
              'success')
        

        # redirecting user to another page
        return redirect(url_for('users.login'))
    
    

    return render_template(
        'register.html',
        title='Register',
        form = form)

@users.route('/login',
           methods=['GET', 'POST'] # accepts get and post requests
           )
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next') # saved in the url, for example if you tried to access the account page without being logged in
            return redirect(next_page) if next_page else redirect(url_for('main.ome'))            
        else:
            flash('Login failed, please check email and password','danger')
    return render_template(
        'login.html',
        title='Login',
        form = form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route(
        '/account',
        methods=['GET', 'POST']
           )
@login_required
def account():
    form = UpdateAccountForm()
    # form to update account settings

    if form.validate_on_submit():
        if form.picture.data:
            # get previous picture for deletion if not default
            if current_user.image_file != 'default.jpg':
                previous_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
                if os.path.exists(previous_picture):
                    os.remove(previous_picture)

            # setting the user's profile picture name
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    
    elif request.method =='GET':
        # populates the form on page load
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template(
        'account.html',
        title='Account',
        image_file = image_file,
        form = form
    )


@users.route(
    "/user/<string:username>"
)
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()

    # Pagination
    page = request.args.get('page', 1, type = int)

    POSTS_PER_PAGE = 5

    posts = Post.query.\
        filter_by(author = user).\
        order_by(Post.date_posted.desc()).\
        paginate(
            page = page,
            per_page = POSTS_PER_PAGE
    ) 

    return render_template(
        'user_posts.html',
        posts = posts,
        user = user
        )


@users.route(
        '/reset_password',
        methods=['GET', 'POST']
        )
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent to {form.email.data} with instructions', 'info')
        return redirect(url_for('users.login'))
        
    return render_template(
        'reset_request.html',
        title = 'Reset Password',
        form = form
    )

@users.route(
        '/reset_password/<token>',
        methods=['GET', 'POST']
        )
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()


    return render_template(
        'reset_request.html',
        title = 'Reset Password',
        form = form
    )