from flask import Blueprint, render_template, request

from flaskblog.models import Post

main = Blueprint(
    'main', # name
    __name__
)


POSTS_PER_PAGE = 5

# @ = decorator, adds functionality to existing functions
@main.route('/') # what we type to go to different pages, etc (/posts, /user, etc)
@main.route('/home') # multiple routes can be used for the same function
def home():
    # Pagination
    page = request.args.get('page', 1, type = int)

    posts = Post.query.\
        order_by(Post.date_posted.desc()).\
        paginate(
            page = page,
            per_page = POSTS_PER_PAGE
    ) 

    return render_template(
        'home.html',
        posts = posts
        )

@main.route('/about')
def about():
    return render_template('about.html', title = 'About')
