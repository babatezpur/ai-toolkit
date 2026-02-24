from app import ma
from app.models.conversation import Conversation
from app.models.conversation_message import ConversationMessage
from marshmallow import fields, validate


# For validating POST /qa/start request
class StartConversationSchema(ma.Schema):
    message = fields.String(required=True, validate=validate.Length(min=1, max=1000))


# For validating POST /qa/message request
class SendMessageSchema(ma.Schema):
    conversation_id = fields.Integer(required=True)
    message = fields.String(required=True, validate=validate.Length(min=1, max=1000))


# For formatting a single message in responses
class MessageResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConversationMessage
        exclude = ('conversation_id',)


# For formatting a conversation in list view (no messages, just title + id)
class ConversationListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Conversation
        exclude = ('user_id',)


# For formatting a full conversation with all messages
class ConversationDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Conversation
        exclude = ('user_id',)

    messages = fields.Nested(MessageResponseSchema, many=True)


start_conversation_schema = StartConversationSchema()
send_message_schema = SendMessageSchema()
message_response_schema = MessageResponseSchema()
conversation_list_schema = ConversationListSchema(many=True)
conversation_detail_schema = ConversationDetailSchema()