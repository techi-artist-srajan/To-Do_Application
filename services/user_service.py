from models.users_model import Users
from database import db

class Users_Services():
    @staticmethod
    def logging_in(username, password):
        user = Users.query.filter_by(username=username, password=password).first()
        print(user.id)
        return user.id

    @staticmethod
    def get(username):
        user = Users.query.filter_by(username=username).first()
        return user
    
    @staticmethod
    def add(username,password):
        if Users_Services.get(username=username):
            return False
        
        new_user = Users(username=username, password = password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user.id
        except:
            db.session.rollback()
            return None

    @staticmethod
    def update(username, password):
        user = Users_Services.get(username)
        if not user:
            return None
        
        try:
            user.password = password
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def delete(username, password):
        user = Users_Services.get(username)
        if not user:
            return None
        
        if user.password == password:
            try:
                db.session.delete(user)
                db.session.commit()
                return True
            except:
                db.session.rollback()
                return False
        return 0