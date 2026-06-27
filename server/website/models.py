from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# Class inherits from db.Model which is a base class for all models from SQLAlchemy
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(512), nullable=False)  # hashes are ~ 256 chars minimum
    voc = db.relationship('Vocabulary', backref='users')

    def __init__(self, name=None, email=None, pwd=None):
        self.name = name
        self.email = email
        self.set_password(pwd)

    def set_password(self, password):
        self.pwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd, password)

    #Can be useful during debugginign to quickly identify records
    def __repr__(self):
        return f"<User id={self.id} name={self.name}>"


class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word = db.Column(db.String(100), unique=True, nullable=False)
    reading = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Vocabulary id={self.id} word={self.word}>"
    
class Kanji (db.Model):
    __tablename__ = 'kanji'
    id = db.Column(db.Integer, primary_key=True)
    kanji_char = db.Column(db.String(10), nullable=False, unique=True)
    reading = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(200), nullable=False)
    voc = db.relationship('MainVocabulary', backref='kanji')

class MainVocabulary(db.Model):
    __tablename__ = 'mainVocabulary'
    id = db.Column(db.Integer, primary_key=True)
    kanji_id = db.Column(db.Integer, db.ForeignKey('kanji.id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    reading = db.Column(db.String(100), nullable=False) 
    meaning = db.Column(db.String(200), nullable=False)