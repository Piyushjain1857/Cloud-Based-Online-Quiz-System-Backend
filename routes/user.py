from flask import Blueprint, request, jsonify
from core.models import db, User, UserSetting

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    settings = UserSetting.query.filter_by(user_id=user.id).first()
    
    return jsonify({
        'profile': {
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'profileImage': user.profile_image
        },
        'settings': {
            'notifications': {
                'email': settings.email_notifications,
                'push': settings.push_notifications,
                'quizReminders': settings.quiz_reminders
            },
            'preferences': {
                'theme': settings.theme,
                'language': settings.language
            }
        } if settings else {}
    }), 200

@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    settings = UserSetting.query.filter_by(user_id=user.id).first()
    
    if 'profile' in data:
        profile_data = data['profile']
        if 'name' in profile_data: user.name = profile_data['name']
        if 'email' in profile_data: user.email = profile_data['email']
        if 'profileImage' in profile_data: user.profile_image = profile_data['profileImage']
            
    if 'settings' in data and settings:
        s_data = data['settings']
        if 'notifications' in s_data:
            n_data = s_data['notifications']
            if 'email' in n_data: settings.email_notifications = n_data['email']
            if 'push' in n_data: settings.push_notifications = n_data['push']
            if 'quizReminders' in n_data: settings.quiz_reminders = n_data['quizReminders']
        if 'preferences' in s_data:
            p_data = s_data['preferences']
            if 'theme' in p_data: settings.theme = p_data['theme']
            if 'language' in p_data: settings.language = p_data['language']
        
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200
