
from flask import current_app as app, redirect, render_template, request, url_for
from .database import db
from application.models import User

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