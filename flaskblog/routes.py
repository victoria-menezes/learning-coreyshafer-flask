from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post

from flask_login import login_user, current_user, logout_user, login_required
    
import secrets
import os

from PIL import Image

# dummy data
# posts : list[dict] = [
#     {
#         'author':'Corey Schafer',
#         'title':'My first post',
#         'content':'First post ever!',
#         'date_posted':'April 20, 2018'
#     },
#     {
#         'author':'Jane Doe',
#         'title':'Blog post 2',
#         'content':'Hello there...',
#         'date_posted':'April 21, 2018'
#     },
#     {
#         'author':'Jane Doe',
#         'title':'A new post!',
#         'content':'Cool!',
#         'date_posted':'April 22, 2018'
#     }
# ]

# @ = decorator, adds functionality to existing functions
@app.route('/') # what we type to go to different pages, etc (/posts, /user, etc)
@app.route('/home') # multiple routes can be used for the same function
def home():
    return render_template(
        'home.html',
        posts = Post.query.all()
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


def save_picture(
    form_picture,
    output_size : tuple[int, int] = (125, 125)
    ):
    # randomize new name for the file
    random_hex = secrets.token_hex(8)
    
    # grab file extension
    _, f_ext = os.path.splitext(form_picture.filename)

    # final file name
    picture_fn = random_hex + f_ext

    # full path of where the image will be saved
    picture_path = os.path.join(
        app.root_path,
        'static/profile_pics',
        picture_fn
        )
    
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    
    img.save(picture_path)
    
    return picture_fn

@app.route(
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
        return redirect(url_for('account'))
    
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

@app.route(
        '/post/new',
        methods=['GET', 'POST']
        )
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title = form.title.data,
            content = form.content.data,
            author = current_user
        )

        db.session.add(post)
        db.session.commit()
        
        flash('Your post has been created', 'success')
        return redirect(url_for('home'))
    



    return render_template(
        'post_new.html',
        title='New Post',
        form = form
    )

# specific page per post
@app.route(
    '/post/<int:post_id>'
)
def post(
    post_id : int
    ):
    post = Post.query.get_or_404(post_id) # returns 404 if it doesnt exist

    return render_template(
        'post.html',
        title=post.title,
        post = post
    )
@app.route(
    '/post/<int:post_id>/update',
    methods = ['GET', 'POST']
)
@login_required
def update_post(
        post_id : int
    ):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()

        flash('Post updated.', 'success')
        return redirect(url_for('post', post_id = post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template(
        'post_new.html',
        title = 'Update Post',
        post = post,
        form = form,
        legend='Update Post'
    )

    
@app.route(
    '/post/<int:post_id>/delete',
    methods = ['POST']
)
@login_required
def delete_post(post_id : int):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    return render_template(
    )