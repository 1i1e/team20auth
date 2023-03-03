from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Users,Auths
import re #regex module
from flask_login import login_user,logout_user,login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random



auth = Blueprint("auth", __name__)

@auth.route("/") ## moved from views.home to here
## so that user sees login page first, forced to login in order to access homepage
@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        usrnam = request.form.get("usrnam") ##debug
        
        user = Users.query.filter_by(email=email).first()
        print(f"query result of user's stored email: {user} ")
        authUser = Auths.query.filter_by(username=usrnam).first()
        if user:
            if check_password_hash(authUser.hashpassword, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True) #store user in session upon sign-in
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect')
        else:
            flash('User does not exist. Create an account',category='error')


    return render_template("login.html") #if get request and not post

### define read and write permissions to our server
@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    #regex = re.compile(r'(^[A-Z0-9_!#$%&'*+/=?`{|}~^.-]+@[A-Z0-9.-]+$)')
    rand_num = random.randint(1,19)
    
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("usrnam") ##debug
        fname = request.form.get("fname")
        lname = request.form.get("lname") ##debug
        print(f"the username: {username} was sent in a POST req")

        pw1 = request.form.get("pw1")
        pw2 = request.form.get("pw2")

        email_exists = Users.query.filter_by(email=email).first()
        username_exists = Users.query.filter_by(userName=username).first() 
        if email_exists:
            flash('Email is already taken.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif pw1 != pw2:
            flash('Passwords do not match', category='error')
        elif len(username) < 2:
            flash('Username is too short',category='error')
        elif len(pw1) < 8:
            flash('Password is too short',category='error')
        ##email regex to escape SQL injection ^[A-Z0-9_!#$%&'*+/=?`{|}~^.-]+@[A-Z0-9.-]+$
        ## https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
        # elif not re.match(regex,email):
        #     flash('Invalid email', category='error')
        else:
            new_user = Users(userID=rand_num,firstName=fname,lastName=lname,email=email,userName=username)
            new_authUser = Auths(authID=rand_num,username=username,hashpassword=generate_password_hash(pw1, method='sha256'))
            db.session.add(new_user)
            db.session.add(new_authUser)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User account created!',category='success')
            return redirect(url_for('views.home'))
            

    return render_template("signup.html")

@auth.route("/logout")
@login_required ##need to be logged in in order to log out
def logout():
    logout_user()
    return redirect(url_for("auth.login"))##redirect user to login page


