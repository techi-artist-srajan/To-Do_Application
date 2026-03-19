from flask import Flask, render_template, request, redirect, url_for
from database import db
from flask_smorest import Api
from routes.todo import todos_blp
from routes.user import user_blp
from routes.pages import pages_blp

app=Flask(__name__)
app.config["API_TITLE"] = "My Store API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = "supersecretkey123"
app.config["SECRET_KEY"] = "supersecretkey123"

db.init_app(app)

# @app.route("/login")
# def login():
#     return render_template("login.html")

# @app.route("/update")
# def update():
#     return render_template("update.html")

api = Api(app)

app.register_blueprint(pages_blp)
api.register_blueprint(todos_blp)
api.register_blueprint(user_blp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)