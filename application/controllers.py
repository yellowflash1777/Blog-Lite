
from email import message
import os
from flask import current_app as app, flash, redirect, render_template, request, send_from_directory, url_for
from .database import db
from application.models import Post, User
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
        username=request.form.get("username")
        password=request.form.get("password")
        user = User.query.filter_by(username=username,password=password).first()
        if user is not None:
            return redirect(url_for('home', username=username))
        else:
            return render_template("login.html", message="Invalid username and/or password")
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home', username=username))
        else:
            return render_template("register.html", message="Username already exists")
    return render_template("register.html")




@app.route('/home')
def home():
    username=request.args.get("username")
    return render_template('home.html',username=username)

@app.route('/add/blog/<username>', methods=["GET", "POST"])
def add_blog(username):
    if request.method == "POST":
        title=request.form.get("title")
        content=request.form.get("content")
        username=username
        timestamp=datetime.datetime.now()
        image=request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('uploaded_file', filename=filename)
        else:
            image_url = None
        post = Post(title=title,content=content,username=username,timestamp=timestamp,image_url=image_url)        
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home', username=username))
    return render_template("add_blog.html",username=username)

@app.route('/user/<username>')
def user(username):
    posts = Post.query.filter_by(username=username).all()
    return render_template("user.html", posts=posts,username=username)