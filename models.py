from datetime import datetime
from app import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(30), unique=False, nullable=False)
    mess_txt = db.Column(db.String(1000), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='posts', lazy=True)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="restrict"), nullable=False)
    author = db.Column(db.String(30), unique=False, nullable=False)
    mess_txt = db.Column(db.String(1000), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
