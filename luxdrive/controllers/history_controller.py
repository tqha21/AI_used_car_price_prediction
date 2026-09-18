from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.vehicle import Vehicle

history_bp = Blueprint('history', __name__)

@history_bp.route('/lich-su')
@login_required
def history():
    """Trang lịch sử định giá của user"""
    search = request.args.get('q', '').lower()
    query = Vehicle.query.filter_by(user_id=current_user.id)
    
    if search:
        query = query.filter(Vehicle.brand.ilike(f'%{search}%') | Vehicle.model.ilike(f'%{search}%'))
    
    vehicles = query.order_by(Vehicle.created_at.desc()).all()
    total = Vehicle.query.filter_by(user_id=current_user.id).count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = []
        for v in vehicles:
            diff = ((v.price - v.ai_price) / v.ai_price * 100) if v.ai_price else 0
            change_type = 'up' if diff > 0 else ('down' if diff < 0 else 'flat')
            change_str = f"+{diff:.1f}%" if diff > 0 else (f"{diff:.1f}%" if diff < 0 else "Ổn định")
            data.append({
                'id': v.id,
                'name': v.full_name,
                'sub': f"{v.year} · {v.transmission} · {v.fuel_type}",
                'image': v.primary_image,
                'date': v.created_at.strftime('%d/%m/%Y'),
                'price': v.price_formatted,
                'change': change_str,
                'change_type': change_type,
                'status': v.status,
                'status_label': v.status_label
            })
        return jsonify({'data': data, 'total': total})

    return render_template('history.html',
        active_nav='lich_su',
        history=vehicles,
        total=total,
        search=search
    )
