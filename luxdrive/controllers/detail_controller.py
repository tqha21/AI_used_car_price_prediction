import random
from flask import Blueprint, render_template, abort
from models.vehicle import Vehicle

detail_bp = Blueprint('detail', __name__)

@detail_bp.route('/xe/<int:listing_id>')
def car_detail(listing_id: int):
    """Trang chi tiết tin đăng xe"""
    vehicle = Vehicle.query.get_or_404(listing_id)
    
    # Build listing object compatible with detail.html template
    ai_price = vehicle.ai_price or int(vehicle.price * 0.95)
    ai_confidence = random.randint(85, 94)
    
    # Build default features list from vehicle data
    default_features = [
        f"Hộp số {vehicle.transmission}",
        f"Nhiên liệu {vehicle.fuel_type}",
        f"Màu ngoại thất {vehicle.color or 'N/A'}",
        "Cảm biến lùi + Camera lùi",
        "Hệ thống kiểm soát hành trình",
        "Túi khí an toàn đa hướng",
    ]
    
    # Dealer info from owner
    owner = vehicle.owner
    dealer_name = owner.full_name if owner else "LuxDrive Seller"
    dealer_phone = owner.phone if owner and owner.phone else "Liên hệ qua LuxDrive"
    
    class Dealer:
        pass
    
    dealer = Dealer()
    dealer.name = dealer_name
    dealer.rating = 4.7
    dealer.reviews = random.randint(15, 120)
    dealer.address = "TP. Hồ Chí Minh"
    dealer.phone = dealer_phone
    
    class Listing:
        pass
    
    listing = Listing()
    listing.id = vehicle.id
    listing.car_name = vehicle.full_name
    listing.brand = vehicle.brand
    listing.year = vehicle.year
    listing.mileage = vehicle.mileage
    listing.fuel = vehicle.fuel_type
    listing.doors = vehicle.doors or 4
    listing.color = vehicle.color or "N/A"
    listing.price = vehicle.price
    listing.ai_price = ai_price
    listing.ai_confidence = ai_confidence
    listing.images = vehicle.image_list or [vehicle.primary_image]
    listing.description = vehicle.description or f"Xe {vehicle.full_name} tình trạng tốt, cần bán gấp."
    listing.features = default_features
    listing.dealer = dealer
    listing.price_formatted = vehicle.price_formatted
    listing.mileage_formatted = vehicle.mileage_formatted
    
    # AI price billion format
    listing.ai_price_billion = f"{ai_price/1e9:.2f} Tỷ".replace(".", ",")
    
    # Price diff
    diff = (vehicle.price - ai_price) / ai_price * 100
    sign = "+" if diff >= 0 else ""
    listing.price_diff_pct = f"{sign}{diff:.1f}%"
    listing.price_diff_positive = vehicle.price >= ai_price
    
    return render_template('detail.html',
        active_nav='xe_dang_ban',
        listing=listing
    )
