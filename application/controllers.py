
from email import message
import os
from flask import current_app as app, flash, redirect, render_template, request, send_from_directory, url_for
from .database import db
from application.models import Follow, Post, User
import datetime
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(
            username=username, password=password).first()
        if user is not None:
            global current_user
            current_user = user
            return redirect(url_for('home', username=username))
        else:
            return render_template("login.html", message="Invalid username and/or password")
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            global current_user
            current_user = user
            return redirect(url_for('home', username=username))
        else:
            return render_template("register.html", message="Username already exists")
    return render_template("register.html")


@app.route('/home')
def home():
    following_list=[]
    follows = Follow.query.filter_by(follower_username=current_user.username).all()
    for follow in follows:
        following_list.append(follow.followed_username)
    print(following_list)
    posts=Post.query.filter(Post.username.in_(following_list)).order_by(Post.timestamp.desc()).all()
    return render_template('home.html', username=current_user.username, posts=posts)


@app.route('/add/blog/<username>', methods=["GET", "POST"])
def add_blog(username):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        username = username
        timestamp = datetime.datetime.now()
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('uploaded_file', filename=filename)
        else:
            image_url = None
        user = User.query.filter_by(username=username).first()
        user.number_of_posts += 1
        post = Post(title=title, content=content, username=username,
                    timestamp=timestamp, image_url=image_url)
        db.session.add(post)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home', username=username))
    return render_template("add_blog.html", username=username)


@app.route('/user/<username>')
def user(username):

    posts = Post.query.filter_by(username=username).all()
    user = User.query.filter_by(username=username).first()
    already_follow=False
    follow = Follow.query.filter_by(
        follower_username=current_user.username, followed_username=username).first()
    if follow is not None:
        already_follow=True

    return render_template("user.html", posts=posts, username=username,already_follow=already_follow, current_user=current_user.username, user=user)


@app.route('/search', methods=["GET", "POST"])
def search():

    if request.method == "POST":
        search = request.form.get("search")
        users = User.query.filter(User.username.like('%'+search+'%')).all()
        return render_template("search.html", users=users, username=current_user.username)
    return render_template("search.html")


@app.route('/delete/<username>/post/<post_id>')
def delete(username, post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    user = User.query.filter_by(username=username).first()
    user.number_of_posts -= 1
    db.session.delete(post)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/edit/<username>/post/<post_id>', methods=["GET", "POST"])
def edit_post(username, post_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image = request.files['image']
        post = Post.query.filter_by(post_id=post_id).first()
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('uploaded_file', filename=filename)
            post.image_url = image_url

        post.title = title
        post.content = content
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user', username=username))
    post = Post.query.filter_by(post_id=post_id).first()
    return render_template("edit_post.html", post=post, username=username)


@app.route('/delete/<username>')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(username=username).all()
    for post in posts:
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/follow/<username>')
def follow(username):
    follow = Follow.query.filter_by(
        follower_username=current_user.username, followed_username=username).first()
    if follow is None:
        user = User.query.filter_by(username=username).first()

        current_user.number_of_following += 1
        user.number_of_followers += 1
        timestamp = datetime.datetime.now()
        follow = Follow(follower_username=current_user.username,
                        followed_username=username, timestamp=timestamp)
        db.session.add(user)
        db.session.add(current_user)
        db.session.add(follow)
        db.session.commit()
    return redirect(url_for('user', username=username))

#yet to complete
@app.route('/unfollow/<username>')
def unfollow(username):
    follow = Follow.query.filter_by(
        follower_username=current_user.username, followed_username=username).first()
    if follow is not None:
        user = User.query.filter_by(username=username).first()
        current_user.number_of_following -= 1
        user.number_of_followers -= 1
        db.session.add(user)
        db.session.add(current_user)
        db.session.delete(follow)
        db.session.commit()
    return redirect(url_for('user', username=username))


@app.route('/<username>/followers')
def followers(username):
    follows = Follow.query.filter_by(followed_username=username).all()
    return render_template('followers.html', follows=follows, username=username)


@app.route('/<username>/following')
def following(username):
    print(username)
    follows = Follow.query.filter_by(follower_username=username).all()
    return render_template('following.html', follows=follows, username=username)
