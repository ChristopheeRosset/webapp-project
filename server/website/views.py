from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from server.website.models import User

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template("home.html")

@views.route("/user")
def user():
    if "user_name" in session:
        username = session["user_name"]
        flash("Connected!", "info")
        return render_template("user.html", name=username)
    else:
        return redirect(url_for("auth.login"))