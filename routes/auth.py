from flask import Blueprint, request, jsonify
from core.models import db, User, UserSetting

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'All fields are required.'}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User with this email already exists.'}), 400

    # Add new user
    new_user = User(
        name=name,
        email=email,
        password=password  # WARNING: In a real app, use password hashing!
    )
    
    db.session.add(new_user)
    db.session.commit()

    # Create default settings for new user
    settings = UserSetting(user_id=new_user.id)
    db.session.add(settings)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully.',
        'user': {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email,
            'role': new_user.role
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user or user.password != password:
        return jsonify({'error': 'Invalid email or password.'}), 401

    return jsonify({
        'message': 'Login successful.',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    }), 200
