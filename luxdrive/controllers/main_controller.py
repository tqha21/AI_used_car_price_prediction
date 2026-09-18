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
    
    popular_brands = ['Toyota', 'Honda', 'Mazda', 'Hyundai', 'Kia', 'Ford', 'VinFast']
    if brand in popular_brands:
        from services.valuation_service import ValuationService
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
        
    return jsonify(result)
