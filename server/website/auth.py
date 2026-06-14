from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from server.website.models import User, db

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@auth.route("/login", methods=["GET","POST"])
def login():
    if "user_name" in session:
        return redirect(url_for("views.user"))
    #Handle POST requests
    elif (request.method == "POST"):
        session.permanent = True
        username = request.form["username"]
        password = request.form["pwd"]

        #Check password
        user = db.session.execute(db.select(User).filter_by(name=username)).scalar()
        if user and user.check_password(password):
            #Save session for the user using its id
            session["user_name"] = user.name
            return redirect(url_for("views.user"))
        else:
            return render_template("login.html", error="Invalid username or password")

    #Handle GET requests + user not in session
    else:
        return render_template("login.html")

@auth.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("auth.login")) 

@auth.route("/register", methods = ["GET", "POST"])
def register():
    if "user_name" in session:
        return redirect(url_for("views.user"))
    elif (request.method == "POST"):
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["pwd"]

        #Check if fields have been filled
        if not username or not email or not password:
            return render_template("register.html", error="Please fill in every field before signin up")

        
        #Check if name or email is already used => first() return either Query object if found, or None
        is_name_existing = db.session.execute(db.select(User).filter_by(name=username)).scalar()
        is_email_existing = db.session.execute(db.select(User).filter_by(email=email)).scalar()
        if is_name_existing:
            return render_template("register.html", error="Username already taken")
        if is_email_existing:
            return render_template("register.html", error="Email already taken")

        #Save to DB
        user = User( name = username,
                    email = email, 
                    pwd = password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    #GET Request + user not in session
    else:
        return render_template("register.html")

@auth.route("/unregister", methods=["POST"])
def unregister():
    if "user_name" in session:
        user = db.session.execute(db.select(User).filter_by(name=session["user_name"])).scalar()
        db.session.delete(user)
        db.session.commit()
        session.pop("user_name", None)
        return redirect(url_for("views.home"))