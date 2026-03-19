from flask import request, jsonify, session
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from database import db
from models.users_model import Users
from schemas.user_schema import UserGetSchema, UserPostSchema, MessageSchema, UserPutSchema
from services.user_service import Users_Services

user_blp = Blueprint("user",__name__, url_prefix = '/api/users', description = "Users Routes")

@user_blp.route("/")
class UserResources(MethodView):

    # @user_blp.arguments(UserGetSchema, location='query')
    # @user_blp.response(201, MessageSchema)
    # def get(self, id):
    #     id = id.get('id')
    #     user = Users_Services.get_by_id(id)
    #     if user is None:
    #         abort(404, message="User not found")
    #     else:
    #         return jsonify({"username":user.username}), 200

    @user_blp.arguments(UserPostSchema)
    @user_blp.response(200, MessageSchema)
    def post(self, data):
        added = Users_Services.add(username=data.get("username"),password = data.get("password"))
        if added is None:
            abort(400, message="Couldn't Register")
        elif added:
            session["user_id"] = id
            return jsonify({"msg":"User Registered Successfully","id":id}), 201
        else:
            abort(400, message="Username already Exist")

    @user_blp.arguments(UserPutSchema)
    @user_blp.response(200, MessageSchema)
    def put(self, data):
        if not session.get("user_id"):
            abort(404, message="Please Login")
        username=data.get("username")
        password=data.get("password")
        updated = Users_Services.update(username, password)
        if updated is None:
            abort(404, message="User Doesn't Exists")
        elif updated is False:
            abort(400, message="Internal Error")
        else:
            return {"msg":"Password Updated Successfully"}, 200

    @user_blp.arguments(UserPutSchema)
    @user_blp.response(200, MessageSchema)
    def delete(self, data):
        if not session.get("user_id"):
            abort(404, message="Please Login")
        deleted = Users_Services.delete(data.get('username'), data.get('password'))
        if deleted is None:
            abort(400, message="No user found to Delete")
        elif deleted == 0:
            abort(400, message="Invalid Password or Username")
        elif deleted is True:
            return {"msg":"User Deleted Succefully"}, 200
        else:
            abort(400, message="Internal Error...")