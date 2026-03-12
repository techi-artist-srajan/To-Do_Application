from flask import request, jsonify, session, render_template
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from database import db
from models.todo_model import Todo
from schemas.todo_schema import TodoGetSchema, TodoPostSchema, TodoPutIdSchema, TodoPutSchema, TodoMessage, TodoDisplay
from datetime import datetime

todos_blp = Blueprint("todo", __name__, description = "Routes for items")

@todos_blp.route('/todo')
class TodoResource(MethodView):

    @todos_blp.response(200, TodoDisplay(many=True))
    def get(self):
            
            user_id = session.get("user_id")

            if not user_id:
                 abort(401, message="Login Required")
            
            todos = Todo.query.filter_by(user_id=user_id).all()
            return todos

    @todos_blp.arguments(TodoPostSchema)
    @todos_blp.response(200, TodoMessage)
    def post(self, data):
        new_todo = Todo(title = data.get("todo"), description = data.get("description"), date_created = datetime.now().date(), user_id = 1)
        try:
             db.session.add(new_todo)
             db.session.commit()
             return {"msg": "Todo Added Successfully"}, 200
        except Exception as e:
             db.session.rollback()
             return abort(400, message = f"Error: {e}")
        
    @todos_blp.arguments(TodoPutSchema)
    @todos_blp.arguments(TodoPutIdSchema, location = 'query')
    @todos_blp.response(200, TodoMessage)
    def put(self, data, id):
        update_todo=Todo.query.filter_by(sno = id.get('id')).first()
        if update_todo:
            try:
                update_todo.title = data.get('todo')
                update_todo.description = data.get('description')
                db.session.commit()
                return {"msg": "Updated Successfully"}, 200
            except:
                db.session.rollback()
                abort(400, message="Invalid title or description")
        else:
             abort(400, message="Todo Doesn't exists")              
    
    @todos_blp.arguments(TodoPutIdSchema, location = 'query')
    @todos_blp.response(200, TodoMessage)
    def delete(self, id):
        delete_todo=Todo.query.filter_by(sno = id.get('id')).first()
        if delete_todo:
             db.session.delete(delete_todo)
             db.session.commit()
             return {"msg":"Successfully Deleted Todo"}
        abort(400, message="Todo Doesn't Exists")