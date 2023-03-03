from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Users(db.Model,UserMixin):
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(255))
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def get_id(self):
        return (self.userID)
    
    def __init__(self, userID, userName, firstName, lastName, email):
        self.userID = userID
        self.userName = userName
        self.firstName = firstName
        self.lastName = lastName
        self.email = email        
    def __repr__(self):
        return '<Users %d>' % self.userID #.id to .userID
    
class Auths(db.Model):
    authID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(225))
    hashpassword = db.Column(db.String(225))
    def __init__(self, authID, username, hashpassword):
        self.authID = authID
        self.username = username
        self.hashpassword = hashpassword
    def __repr__(self):
        return '<Auths %s>' % self.username
    

