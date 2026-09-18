import os
from app import create_app, db
from models.user import User
from models.vehicle import Vehicle

app = create_app()
with app.app_context():
    # Remove old logic to allow inserting
    Vehicle.query.delete()
    db.session.commit()
    
    seller = User.query.filter_by(email='seller@luxdrive.ai').first()
    if not seller:
        seller = User(full_name='Nguyễn Văn A', email='seller@luxdrive.ai',
                      phone='0901234567', role='seller', is_vip=True)
        seller.set_password('seller123')
        db.session.add(seller)
        
    admin = User.query.filter_by(email='admin@luxdrive.ai').first()
    if not admin:
        admin = User(full_name='Quản Trị Viên', email='admin@luxdrive.ai',
                     phone='0987654321', role='admin', is_vip=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
    db.session.flush()
        
    cars = [
        Vehicle(user_id=seller.id, brand='Porsche', model='911 Carrera S', year=2021,
                mileage=15000, fuel_type='Xăng', transmission='Tự động', color='Bạc',
                price=8_500_000_000, ai_price=8_200_000_000,
                description='Xe chính chủ, bảo dưỡng đúng hạn tại Porsche Centre TP. HCM.',
                status='live',
                images='https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='BMW', model='X7 xDrive40i', year=2022,
                mileage=8500, fuel_type='Xăng', transmission='Tự động', color='Đen',
                price=6_200_000_000, ai_price=6_000_000_000,
                description='BMW X7 sang trọng, full option, không ngập nước tại Hà Nội.',
                status='live',
                images='https://images.unsplash.com/photo-1555215695-3004980ad54e?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='Mercedes-Benz', model='C300 AMG', year=2022,
                mileage=32500, fuel_type='Xăng', transmission='Tự động', color='Trắng',
                price=1_420_000_000, ai_price=1_450_000_000,
                description='Biển Hà Nội, cam kết không đâm đụng ngập nước.',
                status='live',
                images='https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='Mercedes-Benz', model='GLC 300', year=2021,
                mileage=45000, fuel_type='Xăng', transmission='Tự động', color='Đen',
                price=1_850_000_000, ai_price=1_820_000_000,
                description='Chính chủ bán GLC 300 biển TP. HCM, bảo dưỡng hãng định kỳ.',
                status='live',
                images='https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='Lexus', model='RX 350', year=2020,
                mileage=50000, fuel_type='Xăng', transmission='Tự động', color='Trắng',
                price=2_900_000_000, ai_price=2_850_000_000,
                description='Lexus RX 350 AWD sang trọng, biển Hà Nội.',
                status='live',
                images='https://images.unsplash.com/photo-1629897048514-3dd74142f1f5?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='Toyota', model='Camry 2.5Q', year=2023,
                mileage=12000, fuel_type='Xăng', transmission='Tự động', color='Đen',
                price=1_250_000_000, ai_price=1_280_000_000,
                description='Camry 2.5Q form mới, như xe lướt, biển Đà Nẵng.',
                status='live',
                images='https://images.unsplash.com/photo-1629897048514-3dd74142f1f5?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='Ford', model='Everest Titanium', year=2023,
                mileage=20000, fuel_type='Dầu', transmission='Tự động', color='Cam',
                price=1_350_000_000, ai_price=1_350_000_000,
                description='Everest Titanium 4x4, full lịch sử hãng.',
                status='live',
                images='https://images.unsplash.com/photo-1559416523-140ddc3d238c?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='Honda', model='CR-V L', year=2020,
                mileage=60000, fuel_type='Xăng', transmission='Tự động', color='Trắng',
                price=850_000_000, ai_price=840_000_000,
                description='CR-V bản L Sensing, biển số TP. HCM.',
                status='live',
                images='https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='Hyundai', model='Santa Fe Premium', year=2022,
                mileage=35000, fuel_type='Dầu', transmission='Tự động', color='Đen',
                price=1_150_000_000, ai_price=1_160_000_000,
                description='Santa Fe máy dầu bản cao nhất, biển Hà Nội.',
                status='live',
                images='https://images.unsplash.com/photo-1549646549-c12e2f3d537e?w=600&q=80'),
        Vehicle(user_id=seller.id, brand='Kia', model='Carnival Signature', year=2023,
                mileage=25000, fuel_type='Dầu', transmission='Tự động', color='Xanh',
                price=1_480_000_000, ai_price=1_450_000_000,
                description='Carnival Signature 7 chỗ, xe gia đình ít đi.',
                status='live',
                images='https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=600&q=80'),
    ]
    db.session.add_all(cars)
    db.session.commit()
    print("Seeded", len(cars), "cars.")
