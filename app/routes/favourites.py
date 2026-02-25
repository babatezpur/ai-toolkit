
from flask import Blueprint, request, jsonify
from app import db
from app.middlewares.auth import auth_required
from app.schemas.saved_item_schema import (
    save_item_schema,
    saved_item_response_schema,
    saved_items_response_schema,
)
from app.models.saved_item import SavedItem
from app.errors.exceptions import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)

favourites_bp = Blueprint('favourites', __name__, url_prefix='/favourites')

@favourites_bp.route('/', methods=['POST'])
@auth_required
def add_favourite(current_user):
    # 1. Validate request body
    data = save_item_schema.load(request.get_json())

    # 2. Check if item already exists
    if SavedItem.query.filter_by(
        user_id=current_user.id, topic=data['topic']
    ).first():
        raise ConflictError('Item already saved')

    # 3. Create new favourite
    favourite = SavedItem(
        user_id=current_user.id,
        category=data['category'],
        content=data['content'],
        author=data.get('author'),
        topic=data['topic']
    )
    db.session.add(favourite)
    db.session.commit()

    # 4. Return success response    
    return jsonify({
        'message': 'Favourite added successfully',
        'favourite': saved_item_response_schema.dump(favourite)
    }), 201

@favourites_bp.route('/', methods=['GET'])
@auth_required
def get_favourites(current_user):
    # Check for category filter
    category = request.args.get('category')

    query = SavedItem.query.filter_by(user_id=current_user.id)

    if category:
        if category not in ['fact', 'quote']:
            raise BadRequestError('Category must be "fact" or "quote"')
        query = query.filter_by(category=category)

    items = query.order_by(SavedItem.created_at.desc()).all()

    return jsonify({
        'favourites': saved_items_response_schema.dump(items),
        'count': len(items)
    }), 200


@favourites_bp.route('/<int:item_id>', methods=['DELETE'])
@auth_required
def delete_favourite(current_user, item_id):
    # 1. Find item
    item = SavedItem.query.get(item_id)

    if not item:
        raise NotFoundError('Favourite not found')

    # 2. Verify ownership
    if item.user_id != current_user.id:
        raise ForbiddenError('Not your favourite')

    # 3. Delete
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Removed from favourites'}), 200