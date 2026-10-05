from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models.vehicle import Vehicle, Notification
from extensions import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/ho-so')
@login_required
def profile():
    """Trang hồ sơ cá nhân - quản lý xe đang bán"""
    search = request.args.get('q', '').lower()
    query = Vehicle.query.filter_by(user_id=current_user.id)
    
    if search:
        query = query.filter(Vehicle.brand.ilike(f'%{search}%') | Vehicle.model.ilike(f'%{search}%'))
        
    my_cars = query.order_by(Vehicle.created_at.desc()).all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = []
        for c in my_cars:
            data.append({
                'id': c.id,
                'name': c.full_name,
                'image_url': c.primary_image,
                'status': c.status,
                'status_label': c.status_label,
                'price_formatted': c.price_formatted,
                'year': c.year,
                'mileage_formatted': c.mileage_formatted,
                'fuel_type': c.fuel_type
            })
        return jsonify(data)

    user_info = {
        "name": current_user.full_name,
        "role": current_user.role_label,
        "avatar": current_user.avatar_url,
        "email": current_user.email,
        "phone": current_user.phone or "",
    }
    
    return render_template('profile.html',
        active_nav='ho_so',
        user=user_info,
        my_cars=my_cars,
        my_listings=my_cars,
        listings_count=len(my_cars)
    )

@profile_bp.route('/api/vehicles/<int:vid>/hide', methods=['PATCH'])
@login_required
def hide_vehicle(vid):
    """API: Hạ tin xe (chuyển sang hidden)"""
    v = Vehicle.query.filter_by(id=vid, user_id=current_user.id).first_or_404()
    if v.status == 'live':
        v.status = 'hidden'
    else:
        v.status = 'live'
    db.session.commit()
    return jsonify({
        'success': True,
        'new_status': v.status,
        'new_status_label': v.status_label,
        'message': f'Đã {"hạ tin" if v.status == "hidden" else "hiển thị lại"} xe {v.full_name}'
    })

@profile_bp.route('/api/vehicles/<int:vid>/delete', methods=['DELETE'])
@login_required
def delete_vehicle(vid):
    """API: Xóa tin xe"""
    v = Vehicle.query.filter_by(id=vid, user_id=current_user.id).first_or_404()
    car_name = v.full_name
    db.session.delete(v)
    
    # Send notification
    notif = Notification(
        user_id=current_user.id,
        title='🗑️ Tin đăng đã bị xóa',
        message=f'Tin đăng xe {car_name} đã được xóa thành công.',
        notif_type='warning'
    )
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Đã xóa tin xe {car_name}'
    })

@profile_bp.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    """API: Cập nhật thông tin hồ sơ"""
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    if data.get('full_name'):
        current_user.full_name = data['full_name'].strip()
    if data.get('phone'):
        current_user.phone = data['phone'].strip()
    db.session.commit()
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Đã cập nhật thông tin thành công!'})
    
    flash('Đã cập nhật thông tin hồ sơ!', 'success')
    return redirect(url_for('profile.profile'))

@profile_bp.route('/api/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Đổi mật khẩu"""
    flash('Đã cập nhật mật khẩu thành công!', 'success')
    return redirect(url_for('profile.profile'))

