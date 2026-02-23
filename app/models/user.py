from time import timezone
from app import db
from datetime import datetime, date


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    daily_request_count = db.Column(db.Integer, default=0)
    last_request_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    #Relationships
    saved_items = db.relationship('SavedItem', backref='user', lazy=True)
    searched_items = db.relationship('SearchedItem', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"



    