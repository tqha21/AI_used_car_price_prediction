import uuid
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.vehicle import Vehicle, Transaction, Notification
from extensions import socketio

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment/<int:vehicle_id>', methods=['GET'])
@login_required
def payment_page(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    fee     = int(vehicle.price * 0.01)   # 1% service fee
    return render_template('payment.html',
        vehicle=vehicle,
        fee=fee,
        total=vehicle.price + fee,
        active_nav=''
    )

@payment_bp.route('/payment/<int:vehicle_id>/process', methods=['POST'])
@login_required
def process_payment(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    method  = request.form.get('method', 'vnpay')
    fee     = int(vehicle.price * 0.01)
    # 1. Giao dịch Ký quỹ (Escrow Transaction)
    txn = Transaction(
        user_id=current_user.id,
        vehicle_id=vehicle.id,
        amount=vehicle.price,
        fee=fee,
        method=method,
        status='escrow_locked', # Trạng thái ký quỹ chờ xử lý
        txn_ref=uuid.uuid4().hex.upper()[:16]
    )
    db.session.add(txn)
    
    # 2. Update trạng thái xe
    vehicle.status = 'pending'
    
    # 3. Gửi thông báo cho Admin (Real-time SocketIO)
    admin_notif = Notification(
        user_id=1, # Giả định ID 1 là Admin
        title='🚨 Giao dịch Ký quỹ mới!',
        message=f'User {current_user.full_name} vừa ký quỹ {fee:,.0f}đ cho xe {vehicle.full_name}.',
        notif_type='warning'
    )
    db.session.add(admin_notif)
    db.session.flush()
    socketio.emit('new_notification', {
        'title': admin_notif.title,
        'message': admin_notif.message,
        'type': admin_notif.notif_type
    }, room='admin')

    # 4. Gửi thông báo cho Người bán (Real-time SocketIO)
    if vehicle.user_id:
        seller_notif = Notification(
            user_id=vehicle.user_id,
            title='💳 Ký quỹ Dịch vụ thành công',
            message=f'Xe {vehicle.full_name} đã được thanh toán phí và đang chờ Admin duyệt.',
            notif_type='success'
        )
        db.session.add(seller_notif)
        db.session.flush()
        socketio.emit('new_notification', {
            'title': seller_notif.title,
            'message': seller_notif.message,
            'type': seller_notif.notif_type
        }, room=f'user_{vehicle.user_id}')
        
    db.session.commit()
    flash(f'✅ Thanh toán thành công! Mã giao dịch: {txn.txn_ref}', 'success')
    return redirect(url_for('payment.success', txn_ref=txn.txn_ref))

@payment_bp.route('/payment/success/<txn_ref>')
@login_required
def success(txn_ref):
    txn = Transaction.query.filter_by(txn_ref=txn_ref).first_or_404()
    return render_template('payment_success.html', txn=txn, active_nav='')
