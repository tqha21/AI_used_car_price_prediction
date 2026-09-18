from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from controllers.auth_controller import admin_required
from extensions import db
from models.vehicle import Vehicle, Notification
from models.user import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@admin_required
def dashboard():
    """Trang quản trị hệ thống"""
    total_users = User.query.count()
    total_cars = Vehicle.query.count()
    pending_cars = Vehicle.query.filter_by(status='pending').all()
    live_cars = Vehicle.query.filter_by(status='live').count()
    
    stats = [
        {'label': 'NGƯỜI DÙNG', 'value': str(total_users), 'sub': 'Tổng số thành viên', 'trend': 'neutral'},
        {'label': 'XE ĐANG BÁN', 'value': str(live_cars), 'sub': 'Đang hiển thị', 'trend': 'up'},
        {'label': 'CHỜ DUYỆT', 'value': str(len(pending_cars)), 'sub': 'Cần xử lý', 'trend': 'neutral'},
        {'label': 'DOANH THU', 'value': '10.5M', 'sub': '+1.2M tháng này', 'trend': 'up'},
    ]
    
    return render_template('admin.html',
        active_nav='admin',
        stats=stats,
        pending=pending_cars
    )

@admin_bp.route('/admin/approve/<int:vid>', methods=['POST'])
@login_required
@admin_required
def approve_vehicle(vid):
    v = Vehicle.query.get_or_404(vid)
    v.status = 'live'
    notif = Notification(user_id=v.user_id, title='✅ Tin đăng được duyệt', message=f'Xe {v.brand} {v.model} của bạn đã được hiển thị.', notif_type='success')
    db.session.add(notif)
    db.session.commit()
    from extensions import socketio
    socketio.emit('new_notification', {'title': notif.title, 'message': notif.message, 'type': 'success'}, room=f'user_{v.user_id}')
    flash('Đã duyệt tin thành công', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/reject/<int:vid>', methods=['POST'])
@login_required
@admin_required
def reject_vehicle(vid):
    v = Vehicle.query.get_or_404(vid)
    v.status = 'rejected'
    notif = Notification(user_id=v.user_id, title='❌ Tin đăng bị từ chối', message=f'Xe {v.brand} {v.model} không đáp ứng đủ điều kiện.', notif_type='error')
    db.session.add(notif)
    db.session.commit()
    from extensions import socketio
    socketio.emit('new_notification', {'title': notif.title, 'message': notif.message, 'type': 'error'}, room=f'user_{v.user_id}')
    flash('Đã từ chối tin đăng', 'error')
    return redirect(url_for('admin.dashboard'))
