from app import db
from datetime import datetime


class SavedItem(db.Model):
    __tablename__ = 'saved_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(10), nullable=False)  # "fact" or "quote"
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(200), nullable=True)  # Only for quotes
    topic = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SavedItem {self.category}: {self.content[:30]}>'