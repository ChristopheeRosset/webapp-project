from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from server.website.models import User, Vocabulary, db
from server.website.services.user_service import upload_csv_into_profile, get_user_vocabulary
from werkzeug.utils import secure_filename

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

@views.route("/vocabulary", methods=["GET", "POST"])
def vocabulary():
    if not "user_name" in session:
        return redirect(url_for("auth.login"))
    
    user = db.session.execute(db.select(User).filter_by(name=session["user_name"])).scalar()
    userId = user.id
    
    if "user_name" in session and request.method == "POST":
        if "csv_file" not in request.files:
            flash("No file part", "error")
            return redirect(url_for("views.vocabulary"))
        
        file = request.files["csv_file"]
        
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(url_for("views.vocabulary"))
        
        if file and file.filename.endswith(".csv"):
            #Use in case of storage within sever
            #filename = secure_filename(file.filename)
            
            # Process upload csv and store it as dictionary
            is_upload_ok = upload_csv_into_profile(file, userId)
            if is_upload_ok:
                flash("CSV uploaded successfully!", "success")
            else:
                flash("Problem when uploading CSV, verify structure content!", "error")
        else:
            flash("Invalid file type. Please upload a CSV file.", "error")
        
        return redirect(url_for("views.vocabulary"))
    #User is in session and it's a GET request
    else:
        #Get current user vocabulary
        vocabulary = get_user_vocabulary(userId)
        return render_template("vocabulary.html", vocabulary=vocabulary)

@views.route("/vocabulary/save", methods=["POST"])
def save_vocabulary():
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    user = db.session.execute(db.select(User).filter_by(name=session["user_name"])) .scalar()
    if not user:
        return redirect(url_for("auth.login"))

    vocs = db.session.execute(db.select(Vocabulary).filter_by(user_id=user.id)).scalars().all()
    for voc in vocs:
        word_value = request.form.get(f"word-{voc.id}")
        reading_value = request.form.get(f"reading-{voc.id}")
        meaning_value = request.form.get(f"meaning-{voc.id}")

        if word_value is not None:
            voc.word = word_value
        if reading_value is not None:
            voc.reading = reading_value
        if meaning_value is not None:
            voc.meaning = meaning_value

    db.session.commit()
    flash("Vocabulary changes saved", "success")
    return redirect(url_for("views.vocabulary"))