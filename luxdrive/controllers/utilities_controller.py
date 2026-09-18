from flask import Blueprint, render_template, request, jsonify
from services.plate_service import PlateService
from services.dictionary_service import DictionaryService
from services.violation_service import ViolationService
from services.valuation_service import ValuationService
from models.vehicle import Vehicle

utilities_bp = Blueprint('utilities', __name__)

# --- PLATE (Định giá biển số & Phong thủy) ---
@utilities_bp.route('/dinh-gia-bien-so')
def plate_valuation():
    """Trang định giá biển số xe"""
    return render_template('plate_valuation.html', active_nav='dinh_gia_bien')

@utilities_bp.route('/dinh-menh-xe')
def plate_destiny():
    """Trang định mệnh xe (phong thủy biển số)"""
    return render_template('plate_destiny.html', active_nav='dinh_menh')

@utilities_bp.route('/api/plate/analyze', methods=['POST'])
def api_analyze_plate():
    data = request.get_json()
    plate = data.get('plate', '').strip().upper()
    if not plate:
        return jsonify({'error': 'Vui lòng nhập biển số hợp lệ'}), 400
    
    result = PlateService.analyze_plate(plate)
    return jsonify(result)


# --- DICTIONARY (Từ điển lỗi xe) ---
@utilities_bp.route('/tu-dien-loi-xe')
def error_dictionary():
    """Trang từ điển lỗi xe"""
    return render_template('dictionary.html', active_nav='tu_dien')

@utilities_bp.route('/api/dictionary', methods=['GET'])
def get_errors():
    search = request.args.get('q', '')
    results = DictionaryService.search_errors(search)
    return jsonify(results)


# --- VIOLATION (Tra cứu phạt nguội) ---
@utilities_bp.route('/phat-nguoi')
def violations():
    """Trang tra cứu phạt nguội"""
    return render_template('violations.html', active_nav='phat_nguoi')

@utilities_bp.route('/api/violations/lookup', methods=['POST'])
def lookup_violation():
    """API: Tra cứu phạt nguội theo biển số xe"""
    data = request.get_json()
    plate = data.get('plate', '').strip().upper()
    result = ViolationService.lookup_violation(plate)
    return jsonify(result)

@utilities_bp.route('/api/violations/common')
def common_violations():
    """API: Danh sách lỗi vi phạm phổ biến"""
    return jsonify(ViolationService.get_common_violations())


# --- DEPRECIATION (Tính trượt giá) ---
@utilities_bp.route('/truot-gia')
def depreciation():
    """Trang tính trượt giá xe theo thời gian"""
    brands = Vehicle.get_brands()
    return render_template('depreciation.html',
        active_nav='truot_gia',
        brands=brands,
        default_models=Vehicle.get_models_by_brand(brands[0] if brands else 'Toyota')
    )

@utilities_bp.route('/api/depreciation', methods=['POST'])
def api_calc_depreciation():
    """API: Tính trượt giá xe qua các năm"""
    data = request.get_json()
    brand = data.get('brand', 'Toyota')
    model = data.get('model', 'Camry')
    year = int(data.get('year', 2020))
    original_price = float(data.get('original_price', 1_000_000_000))
    
    result = ValuationService.calc_depreciation(brand, model, year, original_price)
    return jsonify(result)
