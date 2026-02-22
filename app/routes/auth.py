from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app import db
from app.models.user import User
from app.schemas.user_schema import register_schema, login_schema, user_response_schema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    # 1. Validate request body
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    #2 Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409

    #3 Create new user with hashed password
    new_user = User(email=data['email'], username=data['username'], password_hash=generate_password_hash(data['password'], method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    #4 Create jwt token
    access_token = create_access_token(identity=new_user.id)

    #5 Return success response
    return jsonify({
        'message': 'User created successfully',
        'access_token': access_token,
        'user': user_response_schema.dump(new_user)
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    # 1. Validate request body
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    # 2. Find user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    # 3. Verify password
    if not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # 4. Generate JWT token
    token = create_access_token(identity=str(user.id))

    # 5. Return user info + token
    return jsonify({
        'message': 'Login successful',
        'user': user_response_schema.dump(user),
        'token': token
    }), 200
