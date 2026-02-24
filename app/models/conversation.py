from app import db
from datetime import datetime


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)  # Auto-set from first message
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    messages = db.relationship('ConversationMessage', backref='conversation', lazy=True, order_by='ConversationMessage.created_at')

    def __repr__(self):
        return f'<Conversation {self.id}: {self.title[:30]}>'