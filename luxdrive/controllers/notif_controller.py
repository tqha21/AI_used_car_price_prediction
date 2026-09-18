from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from extensions import db, socketio
from models.vehicle import Notification
from flask_socketio import join_room

notif_bp = Blueprint('notif', __name__)

@notif_bp.route('/api/notifications')
@login_required
def get_notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id)\
                               .order_by(Notification.created_at.desc()).limit(20).all()
    return jsonify([{
        'id': n.id, 'title': n.title, 'message': n.message,
        'type': n.notif_type, 'is_read': n.is_read, 'time_ago': n.time_ago
    } for n in notifs])

@notif_bp.route('/api/notifications/<int:nid>/read', methods=['PATCH'])
@login_required
def mark_read(nid):
    n = Notification.query.filter_by(id=nid, user_id=current_user.id).first_or_404()
    n.is_read = True
    db.session.commit()
    return jsonify({'ok': True})

@notif_bp.route('/api/notifications/read-all', methods=['PATCH'])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False)\
                      .update({'is_read': True})
    db.session.commit()
    return jsonify({'ok': True})

# ── SocketIO Events ────────────────────────────────────
@socketio.on('join')
def on_join(data):
    user_id = data.get('user_id')
    if user_id:
        join_room(f'user_{user_id}')

def send_notification(user_id: int, title: str, message: str, notif_type: str = 'info'):
    """Helper: create DB notification + emit socket event"""
    notif = Notification(user_id=user_id, title=title, message=message, notif_type=notif_type)
    db.session.add(notif)
    db.session.commit()
    socketio.emit('new_notification', {
        'title': title, 'message': message, 'type': notif_type
    }, room=f'user_{user_id}')
