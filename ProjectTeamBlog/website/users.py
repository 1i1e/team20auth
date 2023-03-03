from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Users,Auths

users = Blueprint("users", __name__)

@users.route("/users")
def user_list():
    ppl = db.session.execute(db.select(Users).order_by(Users.userName)).scalars()
    return render_template("users", listppl=ppl)