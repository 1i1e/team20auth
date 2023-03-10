from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sqlite3
import pymysql
#from models import User
from flask import Blueprint, render_template


##website is a python package

# DB_NAME = "projectTeam20.db"
db = SQLAlchemy() ######create SQLAlchemy extension


##tell flask where db is
##then initialize the db and flask app
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "team20"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'insert_mysql_server_here'

    db.init_app(app)   ##initialize web app with sqlalchemy extension 

    
    from .views import views    #blueprint in views file gets registered
    from .auth import auth      # the (.) means relative import

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")

    #provide models before creating db
    from .models import Users,Auths

    
    #call create_database
    # connect_database(app)


    login_manager = LoginManager()
    #if someone is not logged in, but trying 
    #redirect em to login page, force em to login
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    #access info/details related to the user-model given an id
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))


    return app  ##load_user function

##check if database exists, if it does not, then create the db file
##https://stackoverflow.com/questions/27766794/switching-from-sqlite-to-mysql-with-flask-sqlalchemy
## website/' + 'mysql+pymysql://admin:Fang2023@database-capstone.czyt3syhmabj.us-east-1.rds.amazonaws.com:3306/testing'

# def connect_database(app):
#     with app.app_context():
#         # connection = pymysql.connect(host='database-capstone.czyt3syhmabj.us-east-1.rds.amazonaws.com:3306',
#         # user='')
#         # db.create_all()


#     print("database has been connected!!") ##dont do this in production; local app prototype is alright

