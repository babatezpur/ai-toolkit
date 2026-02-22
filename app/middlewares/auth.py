from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User


def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        #1. Verify JWT token is present and valid
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({'error': 'Missing or invalid token'}), 401

        #2. Get user id from token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        kwargs['current_user'] = user
        return func(*args, **kwargs)

    return decorated