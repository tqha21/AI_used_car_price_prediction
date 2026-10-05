from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models.vehicle import Vehicle
from ml.predictor import predict_price

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Trang định giá - Trang chủ"""
    brands = Vehicle.get_brands()
    current_year = 2026
    years = list(range(current_year, 1999, -1))
    
    return render_template('index.html',
        active_nav='dinh_gia',
        brands=brands,
        years=years,
        default_models=Vehicle.get_models_by_brand(brands[0] if brands else 'Toyota')
    )

@main_bp.route('/api/models')
def get_models():
    """API: Lấy danh sách model theo hãng xe"""
    brand = request.args.get('brand', 'Porsche')
    models = Vehicle.get_models_by_brand(brand)
    return jsonify(models)

@main_bp.route('/api/years')
def get_years():
    """API: Lấy danh sách năm sản xuất theo hãng và dòng xe"""
    brand = request.args.get('brand', 'Porsche')
    model = request.args.get('model', '911 Carrera S')
    years = Vehicle.get_years_by_model(brand, model)
    return jsonify(years)

@main_bp.route('/api/predict', methods=['POST'])
@login_required
def predict():
    """API: Dự đoán giá xe bằng ML model thật"""
    from models.vehicle import Vehicle
    data = request.get_json()
    brand        = data.get('brand', 'Porsche')
    model        = data.get('model', '911 Carrera S')
    variant      = data.get('variant', '')
    year         = int(data.get('year', 2023))
    mileage      = int(data.get('mileage', 15000))
    fuel         = data.get('fuel', 'Xăng')
    transmission = data.get('transmission', 'Tự động')
    accident     = int(data.get('accident_history', 0))
    flood        = int(data.get('flood_history', 0))
    owner_count  = int(data.get('owner_count', 1))
    condition    = data.get('overall_condition', 'Tốt')
    origin       = data.get('origin', 'Hà Nội')
    
    from services.valuation_service import ValuationService, POPULAR_CAR_MSRP
    
    popular_brands = ['Toyota', 'Honda', 'Mazda', 'Hyundai', 'Kia', 'Ford', 'VinFast']
    if brand in popular_brands:
        result = ValuationService.calculate_market_value(
            brand, model, year, mileage,
            accident_history=accident,
            flood_history=flood,
            owner_count=owner_count,
            overall_condition=condition,
            origin=origin
        )
    else:
        result = predict_price(
            brand, model, year, mileage, fuel, transmission,
            variant=variant, 
            accident_history=accident, 
            flood_history=flood, 
            owner_count=owner_count,
            overall_condition=condition
        )
        
    # Inject MSRP / Base Price
    brand_data = POPULAR_CAR_MSRP.get(brand, {})
    base_price = brand_data.get(model, 800_000_000)
    result['base_price_formatted'] = f"{int(base_price):,} đ".replace(',', '.')
        
    similar_cars_query = Vehicle.query.filter_by(brand=brand, model=model).limit(5).all()
    similar_cars_data = []
    for i, car in enumerate(similar_cars_query, 1):
        similar_cars_data.append({
            'stt': i,
            'brand': car.brand,
            'model': car.model,
            'year': car.year,
            'mileage': f"{car.mileage:,}",
            'listed_price': f"{int(car.price / 1_000_000):,} tr",
            'ai_price': f"{int((car.ai_price or car.price * 0.97) / 1_000_000):,} tr" 
        })
    result['similar_cars'] = similar_cars_data
    
    return jsonify(result)
