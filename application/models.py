from flask_login import UserMixin
from .database import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    number_of_posts = db.Column(db.Integer, nullable=False, default=0)
    number_of_followers = db.Column(db.Integer, nullable=False, default=0)
    number_of_following = db.Column(db.Integer, nullable=False, default=0)


class Post(db.Model,UserMixin):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(
        "users.username"), nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String)
    number_of_likes = db.Column(db.Integer, nullable=False, default=0)
    number_of_comments = db.Column(db.Integer, nullable=False, default=0)


class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.post_id"), nullable=False)
    username = db.Column(db.String, db.ForeignKey(
        "users.username"), nullable=False)
    comment = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


class Like(db.Model):
    __tablename__ = "likes"
    like_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.post_id"), nullable=False)
    username = db.Column(db.String, db.ForeignKey(
        "users.username"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


class Follow(db.Model):
    __tablename__ = "follows"
    follow_id = db.Column(db.Integer, primary_key=True)
    follower_username = db.Column(
        db.String, db.ForeignKey("users.username"), nullable=False)
    followed_username = db.Column(
        db.String, db.ForeignKey("users.username"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
