from app import db
from datetime import datetime


class SearchedItem(db.Model):
    __tablename__ = 'searched_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    feature = db.Column(db.String(10), nullable=False)  # "facts" or "quotes"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SearchedItem {self.feature}: {self.topic}>'