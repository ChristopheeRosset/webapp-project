from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# Class inherits from db.Model which is a base class for all models from SQLAlchemy
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    pwd = db.Column(db.String(512))  # hashes are ~ 256 chars minimum

    def __init__(self, name=None, email=None, pwd=None):
        self.name = name
        self.email = email
        self.set_password(pwd)

    def set_password(self, password):
        self.pwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd, password)

    def __repr__(self):
        return f"<User id={self.id} name={self.name}>"


class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    word = db.Column(db.String(100), unique=True)
    reading = db.Column(db.String(100))
    meaning = db.Column(db.Text)

    def __repr__(self):
        return f"<Vocabulary id={self.id} word={self.word}>"