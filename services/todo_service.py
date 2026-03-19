from models.todo_model import Todo
from database import db

class Todo_Services():

    @staticmethod
    def get_all(user_id):
        todos = Todo.query.filter_by(user_id=user_id).all()
        return todos
    
    @staticmethod
    def get_by_id(todo_id, user_id):
        todo = Todo.query.filter_by(sno = todo_id, user_id = user_id).first()
        return todo

    @staticmethod
    def add(title, description, date_created, user_id):
        new_todo = Todo(title = title, description = description, date_created = date_created, user_id = user_id)
        try:
             db.session.add(new_todo)
             db.session.commit()
             return True
        except Exception as e:
             db.session.rollback()
             return False

    @staticmethod
    def update(todo_id, title, description, user_id):
        todo = Todo_Services.get_by_id(todo_id, user_id)
        if not todo:
            return False
        
        try:
            todo.title = title
            todo.description = description
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def delete(todo_id, user_id):
        todo = Todo_Services.get_by_id(todo_id, user_id)
        if not todo:
            return False
        try:
            db.session.delete(todo)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False