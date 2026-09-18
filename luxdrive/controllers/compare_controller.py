from flask import Blueprint, render_template, request
from models.vehicle import Vehicle

compare_bp = Blueprint('compare', __name__)

@compare_bp.route('/so-sanh')
def compare():
    """Trang so sánh xe trực tiếp, hỗ trợ nhiều xe"""
    ids_param = request.args.get('ids')
    
    if ids_param is not None:
        if ids_param.strip() == '':
            car_ids = []
        else:
            car_ids = [int(x) for x in ids_param.split(',') if x.strip().isdigit()]
    else:
        car_a_id = request.args.get('a', type=int)
        car_b_id = request.args.get('b', type=int)
        car_ids = []
        if car_a_id: car_ids.append(car_a_id)
        if car_b_id: car_ids.append(car_b_id)
        
    compare_cars = []
    for cid in car_ids[:4]:
        car = Vehicle.query.get(cid)
        if car:
            compare_cars.append(car)
            
    all_cars = Vehicle.query.limit(20).all()
    
    return render_template('compare.html',
        active_nav='so_sanh',
        compare_cars=compare_cars,
        all_cars=all_cars
    )
