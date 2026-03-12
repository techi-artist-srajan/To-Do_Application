from flask import request, jsonify, Blueprint, redirect, render_template, session
from database import db
from models.users_model import Users

pages_blp = Blueprint("pages", __name__)

@pages_blp.route('/login', methods=["GET","POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"]=user.id
            return redirect("/todos")
        
        return "Invalid username or password"
    
    return render_template("login.html")

@pages_blp.route('/todos')
def todo_page():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")
    return render_template('index.html')

@pages_blp.route("/logout")
def logout():

    session.pop("user_id", None)

    return redirect("/login")

@pages_blp.route('/')
def home():
    return render_template('index.html')

@pages_blp.route('/update')
def update():
    return render_template('update.html')