from flask import Blueprint, render_template, request, jsonify
from models.vehicle import Vehicle

listing_bp = Blueprint('listing', __name__)

@listing_bp.route('/xe-dang-ban')
def car_listings():
    """Trang danh sách xe đang bán (live)"""
    search = request.args.get('q', '').lower()
    brand_filter = request.args.get('brand', '')
    year_filter = request.args.get('year', '')
    price_filter = request.args.get('price', '')
    region_filter = request.args.get('region', '')
    sort_by = request.args.get('sort', '')
    
    query = Vehicle.query.filter_by(status='live')
    
    if search:
        query = query.filter(
            Vehicle.brand.ilike(f'%{search}%') |
            Vehicle.model.ilike(f'%{search}%')
        )
    
    if brand_filter:
        query = query.filter(Vehicle.brand.ilike(f'%{brand_filter}%'))
    
    if year_filter:
        try:
            query = query.filter(Vehicle.year == int(year_filter))
        except ValueError:
            pass

    if price_filter:
        if price_filter == '0-1000':
            query = query.filter(Vehicle.price < 1_000_000_000)
        elif price_filter == '1000-2000':
            query = query.filter(Vehicle.price.between(1_000_000_000, 2_000_000_000))
        elif price_filter == '2000-5000':
            query = query.filter(Vehicle.price.between(2_000_000_000, 5_000_000_000))
        elif price_filter == '5000+':
            query = query.filter(Vehicle.price > 5_000_000_000)

    if region_filter:
        if region_filter == 'hanoi':
            query = query.filter(Vehicle.description.ilike('%Hà Nội%'))
        elif region_filter == 'hcm':
            query = query.filter(Vehicle.description.ilike('%HCM%') | Vehicle.description.ilike('%Hồ Chí Minh%'))
        elif region_filter == 'danang':
            query = query.filter(Vehicle.description.ilike('%Đà Nẵng%'))
    
    if sort_by == 'price_asc':
        query = query.order_by(Vehicle.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Vehicle.price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Vehicle.created_at.desc())
    else:
        query = query.order_by(Vehicle.created_at.desc())
    
    vehicles = query.all()
    
    # Get distinct brands & years for filter options
    all_brands = Vehicle.query.filter_by(status='live').with_entities(Vehicle.brand).distinct().all()
    all_brands = sorted([b[0] for b in all_brands])
    
    all_years = Vehicle.query.filter_by(status='live').with_entities(Vehicle.year).distinct().all()
    all_years = sorted([y[0] for y in all_years], reverse=True)
    
    total_count = Vehicle.query.filter_by(status='live').count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = []
        for v in vehicles:
            data.append({
                'id': v.id,
                'name': v.full_name,
                'image': v.primary_image,
                'year': v.year,
                'mileage_formatted': v.mileage_formatted,
                'fuel_type': v.fuel_type,
                'transmission': v.transmission,
                'color': v.color,
                'price_formatted': v.price_formatted,
            })
        return jsonify(data)
    
    return render_template('listings.html',
        active_nav='xe_dang_ban',
        vehicles=vehicles,
        search=search,
        all_brands=all_brands,
        all_years=all_years,
        brand_filter=brand_filter,
        year_filter=year_filter,
        price_filter=price_filter,
        region_filter=region_filter,
        sort_by=sort_by,
        total_count=total_count
    )
