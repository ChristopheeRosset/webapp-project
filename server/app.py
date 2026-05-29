from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from pathlib import Path
import os
from server.models import User, db
import server.config as config

config_values = config.load_config()

app = Flask(__name__)
#Needed to manage sessions, should be kept secret in production, can be generated using secrets.token_hex(32) for example
app.secret_key = config_values["BACKEND"]["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(
    minutes=config_values["BACKEND"].get("SESSION_LIFETIME_MINUTES", 5)
)

#Initiate DB
base_dir = Path(__file__).resolve().parent
db_path = base_dir / "db" / config_values["DB"]["DB_NAME"]
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
db.init_app(app)

#Create tables, create_all does not update tables if they are already in the database 
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    participants = ["Hirai","Paul", "Jacques"]
    return render_template("home.html", nameList=participants)

@app.route("/login", methods=["GET","POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("user"))
    #Handle POST requests
    elif (request.method == "POST"):
        session.permanent = True
        username = request.form["username"]
        password = request.form["pwd"]

        #Check password
        user = db.session.execute(db.select(User).filter_by(name=username)).scalar()
        if user and user.check_password(password):
            #Save session for the user using its id
            session["user_id"] = user.id
            return redirect(url_for("user"))
        else:
            return render_template("login.html", error="Invalid username or password")

    #Handle GET requests + user not in session
    else:
        return render_template("login.html")

@app.route("/user")
def user():
    if "user_id" in session:
        user = db.session.execute(db.select(User).filter_by(id=session["user_id"])).scalar()
        username = user.name
        flash("Connected!", "info")
        return render_template("user.html", name=username)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/register", methods = ["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("user"))
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

        return redirect(url_for("login"))

    #GET Request + user not in session
    else:
        return render_template("register.html")

@app.route("/unregister", methods=["POST"])
def unregister():
    if "user_id" in session:
        user = db.session.execute(db.select(User).filter_by(id=session["user_id"])).scalar()
        db.session.delete(user)
        db.session.commit()
        session.pop("user_id", None)
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)  # debug=True for dev purposes
