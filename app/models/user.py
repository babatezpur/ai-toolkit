from app import db
from datetime import datetime, date


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    daily_request_count = db.Column(db.Integer, default=0)
    last_request_date = db.Column(db.Date, default=date.today())

    #Relationships
    saved_items = db.relationship('SavedItem', backref='user', lazy=True)
    searched_items = db.relationship('SearchedItem', backref='user', lazy=True)
    conversations = db.relationship('Conversation', backref='user', lazy=True)


    def __repr__(self):
        return f"<User {self.username}>"



    