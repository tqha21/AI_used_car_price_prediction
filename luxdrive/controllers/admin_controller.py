from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required
from controllers.auth_controller import admin_required
from extensions import db
from models.vehicle import Vehicle, Notification
from models.user import User
import datetime
import io
import csv

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@admin_required
def dashboard():
    """Trang quản trị hệ thống"""
    time_filter = request.args.get('time', 'all')
    brand_filter = request.args.get('brand', '')
    
    now = datetime.datetime.utcnow()
    
    # Lọc hồ sơ chờ duyệt
    pending_query = Vehicle.query.filter_by(status='pending')
    if time_filter == 'today':
        pending_query = pending_query.filter(Vehicle.created_at >= now.replace(hour=0, minute=0, second=0, microsecond=0))
    elif time_filter == '7days':
        pending_query = pending_query.filter(Vehicle.created_at >= now - datetime.timedelta(days=7))
    elif time_filter == '30days':
        pending_query = pending_query.filter(Vehicle.created_at >= now - datetime.timedelta(days=30))
        
    if brand_filter:
        pending_query = pending_query.filter(Vehicle.brand.ilike(f'%{brand_filter}%'))
        
    pending_cars = pending_query.order_by(Vehicle.created_at.desc()).all()

    total_users = User.query.count()
    total_cars = Vehicle.query.count()
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
        pending=pending_cars,
        current_time_filter=time_filter,
        current_brand=brand_filter
    )

@admin_bp.route('/admin/export')
@login_required
@admin_required
def export_report():
    time_filter = request.args.get('time', 'all')
    now = datetime.datetime.utcnow()
    
    query = Vehicle.query
    if time_filter == 'today':
        query = query.filter(Vehicle.created_at >= now.replace(hour=0, minute=0, second=0, microsecond=0))
    elif time_filter == '7days':
        query = query.filter(Vehicle.created_at >= now - datetime.timedelta(days=7))
    elif time_filter == '30days':
        query = query.filter(Vehicle.created_at >= now - datetime.timedelta(days=30))
        
    vehicles = query.order_by(Vehicle.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['ID', 'Thương Hiệu', 'Dòng Xe', 'Năm Sản Xuất', 'Giá Bán', 'Trạng Thái', 'Ngày Đăng'])
    for v in vehicles:
        writer.writerow([v.id, v.brand, v.model, v.year, v.price, v.status_label, v.created_at.strftime('%Y-%m-%d %H:%M')])
        
    response = Response(output.getvalue().encode('utf-8-sig'), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=bao_cao_luxdrive_{now.strftime("%Y%m%d")}.csv'
    return response

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

@admin_bp.route('/admin/moderation')
@login_required
@admin_required
def moderation():
    """Trang kiểm duyệt và định giá AI"""
    # Lấy xe đang chờ duyệt
    pending_cars = Vehicle.query.filter_by(status='pending').order_by(Vehicle.created_at.desc()).all()
    # Lấy xe đã duyệt gần đây
    approved_cars = Vehicle.query.filter_by(status='live').order_by(Vehicle.created_at.desc()).limit(10).all()
    return render_template('admin_moderation.html', pending=pending_cars, approved=approved_cars)

@admin_bp.route('/admin/users')
@login_required
@admin_required
def users():
    """Trang quản lý người dùng và showroom"""
    users_list = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users_list)

@admin_bp.route('/admin/ai-monitoring')
@login_required
@admin_required
def ai_monitoring():
    """Trang giám sát mô hình AI"""
    return render_template('admin_ai_monitoring.html')

@admin_bp.route('/admin/settings')
@login_required
@admin_required
def settings():
    """Trang cấu hình hệ thống"""
    return render_template('admin_settings.html')

@admin_bp.route('/admin/reports')
@login_required
@admin_required
def reports():
    """Trang báo cáo và doanh thu"""
    return render_template('admin_reports.html')
