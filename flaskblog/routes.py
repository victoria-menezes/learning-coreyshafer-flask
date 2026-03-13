from flask import render_template, flash, redirect, url_for
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
    
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
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password': # temporary for testing
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed, please check username and password','danger')
    return render_template(
        'login.html',
        title='Login',
        form = form)