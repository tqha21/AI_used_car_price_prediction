import os
from flask import Flask
from dotenv import load_dotenv
from extensions import db, login_manager, bcrypt, migrate, socketio

load_dotenv()

# ── Controllers (Blueprints) ──────────────────────────────
from controllers.main_controller     import main_bp
from controllers.compare_controller  import compare_bp
from controllers.market_controller   import market_bp
from controllers.history_controller  import history_bp
from controllers.sell_controller     import sell_bp
from controllers.detail_controller   import detail_bp
from controllers.admin_controller    import admin_bp
from controllers.profile_controller  import profile_bp
from controllers.auth_controller     import auth_bp
from controllers.upload_controller   import upload_bp
from controllers.payment_controller  import payment_bp
from controllers.notif_controller    import notif_bp
from controllers.listing_controller  import listing_bp
from controllers.utilities_controller import utilities_bp

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join('views', 'templates'),
        static_folder=os.path.join('views', 'static')
    )
    # ── Config ────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
    
    db_path = os.path.join(os.path.dirname(__file__), 'luxdrive.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', f"sqlite:///{db_path}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024   # 10MB upload limit

    # ── Extensions ────────────────────────────────────────
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins='*', async_mode='eventlet')

    login_manager.init_app(app)
    login_manager.login_view       = 'auth.login'
    login_manager.login_message    = '⚠️ Vui lòng đăng nhập để tiếp tục.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    # ── Register Blueprints ───────────────────────────────
    for bp in (main_bp, compare_bp, market_bp, history_bp, sell_bp,
               detail_bp, admin_bp, profile_bp,
               auth_bp, upload_bp, payment_bp, notif_bp,
               listing_bp, utilities_bp):
        app.register_blueprint(bp)

    # ── DB Init + Seed ────────────────────────────────────
    with app.app_context():
        import models.user    # noqa – register models
        import models.vehicle # noqa
        db.create_all()
        _seed_db()

    return app

def _seed_db():
    """Create default admin + demo data on first run."""
    from models.user    import User
    from models.vehicle import Vehicle, Notification
    if User.query.count() > 0:
        return
    # Admin
    admin = User(full_name='Admin LuxDrive', email='admin@luxdrive.ai',
                 phone='0900000001', role='admin')
    admin.set_password('admin123')
    # Seller demo
    seller = User(full_name='Nguyễn Văn A', email='seller@luxdrive.ai',
                  phone='0901234567', role='seller', is_vip=True)
    seller.set_password('seller123')
    db.session.add_all([admin, seller])
    db.session.flush()
    # Demo vehicles
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

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, use_reloader=False, port=5000)
