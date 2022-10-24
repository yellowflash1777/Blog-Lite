
from flask import current_app as app, redirect, render_template, request, url_for

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST": 
        username=request.form.get("username")
        password=request.form.get("password")
        if username == "admin" and password == "admin":
           return redirect(url_for('admin')) 
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')