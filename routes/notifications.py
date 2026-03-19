from flask import Blueprint, request, jsonify
from core.models import db, Notification, User

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('', methods=['GET'])
def get_notifications():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'notifications': [], 'unreadCount': 0}), 200
        
    notifications = Notification.query.filter_by(user_id=user.id).all()
    
    notif_list = []
    for n in notifications:
        notif_list.append({
            'id': str(n.id),
            'type': n.type,
            'title': n.title,
            'message': n.message,
            'time': n.time_label,
            'read': n.read
        })
        
    return jsonify({
        'message': 'Notifications fetched successfully.',
        'notifications': notif_list,
        'unreadCount': len([n for n in notifications if not n.read])
    }), 200

@notifications_bp.route('/read', methods=['POST'])
def mark_notifications_read():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    notif_id = data.get('id')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'No user found'}), 404

    if notif_id == 'all':
        Notification.query.filter_by(user_id=user.id).update({Notification.read: True})
    else:
        Notification.query.filter_by(id=notif_id, user_id=user.id).update({Notification.read: True})
    
    db.session.commit()
    
    unread_count = Notification.query.filter_by(user_id=user.id, read=False).count()
                
    return jsonify({
        'message': 'Notifications marked as read.',
        'unreadCount': unread_count
    }), 200

@notifications_bp.route('/broadcast', methods=['POST'])
def broadcast_notification():
    admin_id = request.headers.get('X-User-ID')
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'admin':
        return jsonify({'error': 'Forbidden. Admin access required.'}), 403
        
    data = request.json
    title = data.get('title')
    message = data.get('message')
    notif_type = data.get('type', 'system')
    
    if not title or not message:
        return jsonify({'error': 'Title and message are required.'}), 400
        
    users = User.query.all()
    for user in users:
        new_notif = Notification(
            user_id=user.id,
            type=notif_type,
            title=title,
            message=message,
            time_label='Just now',
            read=False
        )
        db.session.add(new_notif)
        
    db.session.commit()
    
    return jsonify({'message': f'Notification broadcasted to {len(users)} users.'}), 201
