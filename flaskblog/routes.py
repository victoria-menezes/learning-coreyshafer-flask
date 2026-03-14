from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post

from flask_login import login_user, current_user, logout_user, login_required
    
# dummy data
posts : list[dict] = [
    {
        'author':'Corey Schafer',
        'title':'My first post',
        'content':'First post ever!',
        'date_posted':'April 20, 2018'
    },
    {
        'author':'Jane Doe',
        'title':'Blog post 2',
        'content':'Hello there...',
        'date_posted':'April 21, 2018'
    },
    {
        'author':'Jane Doe',
        'title':'A new post!',
        'content':'Cool!',
        'date_posted':'April 22, 2018'
    }
]

# @ = decorator, adds functionality to existing functions
@app.route('/') # what we type to go to different pages, etc (/posts, /user, etc)
@app.route('/home') # multiple routes can be used for the same function
def home():
    return render_template(
        'home.html',
        posts = posts
        )

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

@app.route('/register',
           methods=['GET', 'POST'] # accepts get and post requests
           )
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
        return redirect(url_for('login'))
    
    

    return render_template(
        'register.html',
        title='Register',
        form = form)

@app.route('/login',
           methods=['GET', 'POST'] # accepts get and post requests
           )
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next') # saved in the url, for example if you tried to access the account page without being logged in
            return redirect(next_page) if next_page else redirect(url_for('home'))            
        else:
            flash('Login failed, please check email and password','danger')
    return render_template(
        'login.html',
        title='Login',
        form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route(
        '/account',
        methods=['GET', 'POST']
           )
@login_required
def account():
    form = UpdateAccountForm()
    # form to update account settings

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    
    elif request.method =='GET':
        # populates the form on page load
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename = f'profile_pics/{current_user.image_file}')
    return render_template(
        'account.html',
        title='Account',
        image_file = image_file,
        form = form
    )