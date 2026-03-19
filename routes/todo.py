from flask import request, jsonify, session, render_template
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from database import db
from models.todo_model import Todo
from schemas.todo_schema import TodoGetSchema, TodoPostSchema, TodoPutIdSchema, TodoPutSchema, TodoMessage, TodoDisplay
from datetime import datetime
from services.todo_service import Todo_Services

todos_blp = Blueprint("todo", __name__, url_prefix='/api/todo' , description = "Routes for items")

@todos_blp.route('/')
class TodoResource(MethodView):

    @todos_blp.response(200, TodoDisplay(many=True))
    def get(self):
            user_id = session.get("user_id")
            if not user_id:
                 abort(401, message="Login Required")
            todos = Todo_Services.get_all(user_id)
            return todos

    @todos_blp.arguments(TodoPostSchema)
    @todos_blp.response(200, TodoMessage)
    def post(self, data):
        title = data.get("todo")
        description = data.get("description")
        date_created = datetime.now().date()
        user_id = session.get("user_id")
        if Todo_Services.add(title, description, date_created, user_id):
            return {"msg": "Todo Added Successfully"}, 201
        abort(400, message = f"Internal Error, Unable to add user")
        
    @todos_blp.arguments(TodoPutSchema)
    @todos_blp.arguments(TodoPutIdSchema, location = 'query')
    @todos_blp.response(200, TodoMessage)
    def put(self, data, id):
        sno = id.get("id")
        user_id = session.get("user_id")
        title = data.get('todo')
        description = data.get('description')
        if Todo_Services.update(sno, title, description, user_id):
            return {"msg": "Updated Successfully"}
        else:
            abort(404, message="Todo Doesn't exists")              
    
    @todos_blp.arguments(TodoPutIdSchema, location = 'query')
    @todos_blp.response(200, TodoMessage)
    def delete(self, id):
        id = id.get("id")
        user_id = session.get("user_id")
        if Todo_Services.delete(id, user_id):
             return {"msg":"Successfully Deleted Todo"}
        abort(400, message="Todo Doesn't Exists")