from app import ma
from marshmallow import fields, validate


# For facts and quotes requests (same structure)
class TopicRequestSchema(ma.Schema):
    topic = fields.String(required=True, validate=validate.Length(min=1, max=200))
    comment = fields.String(load_default=None, validate=validate.Length(max=500))


# For Q&A message requests
class QAMessageSchema(ma.Schema):
    conversation_id = fields.String(required=True)
    message = fields.String(required=True, validate=validate.Length(min=1, max=1000))


topic_request_schema = TopicRequestSchema()
qa_message_schema = QAMessageSchema()