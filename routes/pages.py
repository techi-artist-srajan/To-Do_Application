from flask import request, jsonify, Blueprint, redirect, render_template, session, url_for
from database import db
from models.users_model import Users
from models.todo_model import Todo
from services.todo_service import Todo_Services
from services.user_service import Users_Services

pages_blp = Blueprint("pages", __name__)

@pages_blp.route('/login', methods=["GET","POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_id = Users_Services.logging_in(username, password)

        if user_id:
            session["user_id"]=user_id
            session["username"]=username
            return redirect(url_for("pages.todo_page"))
        
        return "Invalid username or password"
    
    return render_template("login.html")

@pages_blp.route('/todos')
def todo_page():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")
    username = session.get('username')
    todos = Todo_Services.get_all(user_id)
    return render_template('index.html', username = username, allTodo = todos)

@pages_blp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")


@pages_blp.route('/update/<int:id>')
def update(id):
    user_id = session.get("user_id")
    todo = Todo_Services.get_by_id(id, user_id)
    if not todo:
        return jsonify({"message": "Todo Doesn't exist"}), 404
    return render_template('update.html',todo=todo)


@pages_blp.route("/")
def home():
    return render_template("landing_page.html")

@pages_blp.route('/register', methods=["GET"])
def register():
    return render_template("register_page.html")

@pages_blp.route('/user_password')
def change_password():
    user_id = session.get("user_id")
    username = session.get("username")
    if not user_id:
        redirect("login.html")
    return render_template("update_pass.html", username = username)