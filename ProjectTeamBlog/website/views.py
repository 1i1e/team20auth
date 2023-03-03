from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
views = Blueprint("views", __name__)

# @views.route("/") ##hidden so that anyone can access base page and main website
@views.route("/home")
def home():
    return render_template("home.html", name=current_user.userName)
    ## userName attribute of the Users object.
    ## check for a userName or login to ensure membership for homepage, otherwise, err 500 is returned

# @views.route("/users")
# def home():
#     return render_template("users.html", name=current_user.username)#tell flask to look at templates folder


@views.route("/")
def login():
    return redirect(url_for('auth.login'))