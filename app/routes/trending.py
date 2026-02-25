from flask import Blueprint, jsonify, request
from sqlalchemy import func
from app import db
from app.middlewares.auth import auth_required
from app.models.searched_item import SearchedItem
from app.errors.exceptions import BadRequestError


trending_bp = Blueprint('trending', __name__, url_prefix='/trending')

@trending_bp.route('/', methods=['GET'])
@auth_required
def get_trending(current_user):

    # get feature from query parameters
    feature = request.args.get('feature')

    # build query to get trending items
    query = db.session.query(
        SearchedItem.topic,
        func.count(SearchedItem.topic).label('count')
    )

    if feature:
        if feature not in ['facts', 'quotes']:
            raise BadRequestError('Feature must be "facts" or "quotes"')
        query = query.filter(SearchedItem.feature == feature)

    trending = query.group_by(SearchedItem.topic).order_by(func.count(SearchedItem.topic).desc()).limit(10).all()


    # 2. Return response
    return jsonify({
        'trending': [{'topic': item.topic, 'count': item.count} for item in trending],
        'count': len(trending)
    }), 200