
from app import ma
from app.models.user import User
from marshmallow import fields, validate


# For validating register requests
class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    password = fields.String(required=True, validate=validate.Length(min=6), load_only=True)


# For validating login requests
class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


# For formatting user data in responses (never exposes password_hash)
class UserResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('password_hash', 'daily_request_count', 'last_request_at')


register_schema = RegisterSchema()
login_schema = LoginSchema()
user_response_schema = UserResponseSchema()