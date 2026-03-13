from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm

from dotenv import load_dotenv
from datetime import datetime, timezone
import os

# setting up .env
load_dotenv()
# FLASK_APP
# FLASK_DEBUG, =1 will make the server show changes without restarting, will work with a simple refresh of the page
# TEMPLATE_FOLDER
# Etc

app = Flask(__name__,
    template_folder = os.getenv('TEMPLATE_FOLDER')
    ) # __name__ lets flask know where to look for templates, etc

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')



db = SQLAlchemy(app)

# database is created via python terminal
# from flaskblog import app, db
# app.app_context().push()
# db.create_all()

# to add users, etc:
# db.session.add(etc)
# db.session.commit

# to query out databases:
# User.query.all() / .first() / .filter_by() / db.session.query(User).get(id)

class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True # if left blank, will be assigned automatically since its the primary key
        )
    username = db.Column(
        db.String(20),
        unique = True,
        nullable = False
    )
    email = db.Column(
        db.String(120),
        unique = True,
        nullable = False
    )
    image_file = db.Column(
        db.String(20),
        nullable = False,
        default = 'default.jpg'
    )
    password = db.Column(
        db.String(60),
        nullable = False
    )
    posts = db.relationship(
        'Post',
        backref = 'author', # lets us access Post.author to get the user object that is the author 
        lazy = True # sqlalchemy will load the data as necessary in one go
    )

    def __repr__(self) -> str:
        # how its printed with print()
        return f'User(\'{self.username}\', \'{self.email}\', \'{self.image_file}\')'

class Post(db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    title = db.Column(
        db.String(100),
        nullable = False
    )
    date_posted = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.now(timezone.utc)
    )
    content = db.Column(
        db.Text,
        nullable = False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable = False
    )
    
    def __repr__(self) -> str:
        # how its printed with print()
        return f'Post(\'{self.title}\', \'{self.date_posted}\')'
    
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
        flash(f'Account created for {form.username.data}!',
              'success')
        # redirecting user to another page
        return redirect(url_for('home'))
    
    

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

# alternate way of running the application via the python script
# not recommended over just `flask run` in the terminal
# if __name__ == '__main__':
#     app.run(debug = True)