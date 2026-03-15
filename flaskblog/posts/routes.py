from flask import Blueprint, render_template, flash, redirect, url_for, request, abort

from flaskblog import db
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post

from flask_login import current_user, login_required

posts = Blueprint(
    'posts', # name
    __name__
)


@posts.route(
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
        return redirect(url_for('main.home'))
    



    return render_template(
        'post_new.html',
        title='New Post',
        form = form
    )

# specific page per post
@posts.route(
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
@posts.route(
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
        return redirect(url_for('posts.post', post_id = post.id))
    
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

    
@posts.route(
    '/post/<int:post_id>/delete',
    methods = ['POST'] # method='POST' on the form action or it will tell you this page does not accept this method
)
@login_required
def delete_post(post_id : int):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted.', 'success')
    return redirect(url_for('main.home'))
