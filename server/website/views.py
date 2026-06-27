from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from server.website.models import User, Vocabulary, Kanji, db
from server.website.services.user_service import upload_csv_into_profile, get_user_vocabulary, save_voc
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/kanji-list")
def kanji_list():
    perPage = 50;
    kanjiList = db.paginate(db.select(Kanji), per_page=perPage)
    return render_template("kanji_list.html", kanjiList=kanjiList)

#Route will be used as API endpoint to return specific data instead of loading whole page kanji-list
@views.route("/kanji-chars")
def getKanjiList ():
    kanjiList = db.session.execute(db.select(Kanji.id, Kanji.kanji_char, Kanji.reading, Kanji.meaning)).all()
    return jsonify([{
        'id': kanjis.id,
        'kanji_char': kanjis.kanji_char,
        'reading': kanjis.reading,
        'meaning': kanjis.meaning
        } for kanjis in kanjiList])

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
        #Get current user vocabulary and general kanji list
        vocabulary = get_user_vocabulary(userId)
        #kanjiList = db.session.execute(db.select(Kanji)).scalars().all()
        return render_template("vocabulary.html", vocabulary=vocabulary)

@views.route("/vocabulary/save", methods=["POST"])
def save_vocabulary():
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    user = db.session.execute(db.select(User).filter_by(name=session["user_name"])) .scalar()
    userId = user.id

    #Update each voc line with current values and commit changes to DB
    save_voc(userId)

    flash("Vocabulary changes saved", "success")
    return redirect(url_for("views.vocabulary"))
