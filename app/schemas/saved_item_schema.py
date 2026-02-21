from app import ma
from app.models.saved_item import SavedItem
from marshmallow import fields, validate


# For validating save requests
class SaveItemSchema(ma.Schema):
    category = fields.String(required=True, validate=validate.OneOf(['fact', 'quote']))
    content = fields.String(required=True, validate=validate.Length(min=1))
    author = fields.String(load_default=None)  # Optional, only for quotes
    topic = fields.String(required=True, validate=validate.Length(min=1))


# For formatting saved items in responses
class SavedItemResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SavedItem
        exclude = ('user_id',)  # No need to expose user_id back to the same user


save_item_schema = SaveItemSchema()
saved_item_response_schema = SavedItemResponseSchema()
saved_items_response_schema = SavedItemResponseSchema(many=True)  # For list of items