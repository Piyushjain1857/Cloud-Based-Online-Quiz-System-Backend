from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user') # 'admin' or 'user'
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notifications = db.relationship('Notification', backref='user', lazy=True)
    settings = db.relationship('UserSetting', backref='user', uselist=False, lazy=True)

class UserSetting(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=False)
    quiz_reminders = db.Column(db.Boolean, default=True)
    theme = db.Column(db.String(20), default='light')
    language = db.Column(db.String(50), default='English')

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    participants = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='upcoming')
    points = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False) # Index of the correct option

    options = db.relationship('Option', backref='question', lazy=True, cascade="all, delete-orphan")

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50))
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    time_label = db.Column(db.String(50)) # e.g., "2 hours ago"
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
