from exts import db
from datetime import datetime

# ORM mode
class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text,nullable=False)
    city = db.Column(db.String(100))
    geolocation = db.Column(db.String(100))
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    author = db.relationship("UserModel",backref="questions")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    question = db.relationship("QuestionModel",backref=db.backref("answers",order_by=create_time.desc()))
    author = db.relationship("UserModel",backref="answers")

class UserFavoriteQuestionModel(db.Model):
    __tablename__ = "user_favorite_question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    favorite_id = db.Column(db.Integer, db.ForeignKey('favorite.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class FavoriteModel(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    num_content = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("UserModel", backref="favorite")
    qs = db.relationship('QuestionModel', secondary="user_favorite_question",backref=db.backref('favorite'))


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    captcha = db.Column(db.String(10),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)