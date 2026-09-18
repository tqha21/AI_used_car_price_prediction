from datetime import datetime
from extensions import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    brand        = db.Column(db.String(80), nullable=False)
    model        = db.Column(db.String(100), nullable=False)
    year         = db.Column(db.Integer, nullable=False)
    mileage      = db.Column(db.Integer, nullable=False)
    fuel_type    = db.Column(db.String(30), default='Xăng')
    transmission = db.Column(db.String(30), default='Tự động')
    color        = db.Column(db.String(30))
    doors        = db.Column(db.Integer, default=4)
    price        = db.Column(db.BigInteger, nullable=False)    # VND
    ai_price     = db.Column(db.BigInteger)
    description  = db.Column(db.Text)
    status       = db.Column(db.String(20), default='pending')  # pending|live|hidden|sold
    images       = db.Column(db.Text, default='')              # comma-separated paths
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions  = db.relationship('Transaction', backref='vehicle', lazy=True)

    @property
    def image_list(self):
        return [i.strip() for i in self.images.split(',') if i.strip()] if self.images else []

    @property
    def primary_image(self):
        imgs = self.image_list
        return imgs[0] if imgs else 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&q=80'

    @property
    def price_formatted(self):
        return f"{self.price:,} đ".replace(",", ".")

    @property
    def mileage_formatted(self):
        return f"{self.mileage:,} km".replace(",", ".")

    @property
    def status_label(self):
        return {'pending': 'Chờ duyệt', 'live': 'Đang hiển thị', 'hidden': 'Đã hạ tin', 'sold': 'Đã bán', 'draft': 'Bản nháp'}.get(self.status, self.status)

    @property
    def full_name(self):
        return f"{self.brand} {self.model} {self.year}"

    @property
    def name(self):
        return self.full_name

    @property
    def spec(self):
        from dataclasses import dataclass, field
        from typing import List
        
        @dataclass
        class CarSpec:
            acceleration: str
            horsepower: int
            drivetrain: str
            weight: int
            fuel_type: str
            transmission: str
            fuel_economy: float = 9.5
            maintenance_cost: int = 15
            safety_rating: int = 5
            tags: List[str] = field(default_factory=list)

        return CarSpec(
            acceleration="4.5 giây", horsepower=350,
            drivetrain="4 bánh", weight=1800,
            fuel_type=self.fuel_type, transmission=self.transmission,
            fuel_economy=10.0, maintenance_cost=20, safety_rating=5,
            tags=[self.transmission, self.fuel_type]
        )

    @classmethod
    def get_brands(cls):
        brands = cls.query.with_entities(cls.brand).distinct().all()
        db_brands = [b[0] for b in brands] if brands else []
        default_brands = [
            "Toyota", "Honda", "Hyundai", "Kia", "Mazda", "Ford", "Mitsubishi", 
            "VinFast", "Suzuki", "Nissan", "Chevrolet", "Peugeot",
            "Mercedes-Benz", "BMW", "Audi", "Lexus", "Porsche", "Volvo", "Land Rover"
        ]
        # Combine and remove duplicates while preserving order
        all_brands = list(dict.fromkeys(db_brands + default_brands))
        return all_brands

    @classmethod
    def get_models_by_brand(cls, brand):
        models = cls.query.filter_by(brand=brand).with_entities(cls.model).distinct().all()
        db_models = [m[0] for m in models] if models else []
        
        # Hardcode some default models for common brands
        default_models = {
            "Toyota": ["Vios", "Camry", "Innova", "Fortuner", "Corolla Cross", "Yaris", "Raize", "Veloz", "Hilux"],
            "Honda": ["City", "Civic", "CR-V", "HR-V", "Accord", "Brio"],
            "Hyundai": ["Accent", "Grand i10", "Santa Fe", "Tucson", "Kona", "Creta", "Elantra", "Palisade"],
            "Kia": ["Morning", "Cerato", "K3", "Seltos", "Sorento", "Carnival", "Sonet", "Sportage"],
            "Mazda": ["Mazda3", "CX-5", "Mazda6", "CX-8", "Mazda2", "CX-3", "CX-30"],
            "Ford": ["Ranger", "Everest", "Explorer", "EcoSport", "Territory", "Transit"],
            "Mitsubishi": ["Xpander", "Outlander", "Triton", "Attrage", "Pajero Sport"],
            "VinFast": ["Fadil", "Lux A2.0", "Lux SA2.0", "VF e34", "VF5", "VF8", "VF9"],
            "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLS", "Maybach"],
            "BMW": ["3 Series", "5 Series", "7 Series", "X3", "X5", "X7"],
            "Audi": ["A4", "A6", "A8", "Q5", "Q7", "Q8"],
            "Lexus": ["ES", "RX", "NX", "LX", "IS", "GX"],
            "Porsche": ["Macan", "Cayenne", "Panamera", "911", "Taycan"],
            "Volvo": ["XC60", "XC90", "S90", "V60"],
            "Land Rover": ["Range Rover", "Range Rover Evoque", "Defender", "Discovery"]
        }
        
        defaults = default_models.get(brand, [f"{brand} Model X", f"{brand} Model Y"])
        all_models = list(dict.fromkeys(db_models + defaults))
        return all_models

    @classmethod
    def get_years_by_model(cls, brand, model):
        import datetime
        current_year = datetime.datetime.now().year
        # Base years from 2005 to current year
        base_years = list(range(current_year, 2004, -1))
        
        # Specific model year constraints
        model_years = {
            "VF e34": list(range(current_year, 2021, -1)),
            "VF 5": list(range(current_year, 2022, -1)),
            "VF 8": list(range(current_year, 2022, -1)),
            "VF 9": list(range(current_year, 2022, -1)),
            "Fadil": list(range(2022, 2018, -1)),
            "Lux A2.0": list(range(2022, 2018, -1)),
            "Lux SA2.0": list(range(2022, 2018, -1)),
            "Corolla Cross": list(range(current_year, 2019, -1)),
            "Raize": list(range(current_year, 2020, -1)),
            "Veloz": list(range(current_year, 2021, -1)),
            "Creta": list(range(current_year, 2021, -1)),
            "Seltos": list(range(current_year, 2019, -1)),
            "Sonet": list(range(current_year, 2020, -1)),
            "Carnival": list(range(current_year, 2020, -1)),
            "Territory": list(range(current_year, 2021, -1))
        }
        
        return model_years.get(model, base_years)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title      = db.Column(db.String(200), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    notif_type = db.Column(db.String(30), default='info')  # info|success|warning|error
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def time_ago(self):
        delta = datetime.utcnow() - self.created_at
        if delta.seconds < 60:
            return "Vừa xong"
        elif delta.seconds < 3600:
            return f"{delta.seconds // 60} phút trước"
        elif delta.days == 0:
            return f"{delta.seconds // 3600} giờ trước"
        return f"{delta.days} ngày trước"


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id   = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    amount       = db.Column(db.BigInteger, nullable=False)     # VND
    fee          = db.Column(db.BigInteger, default=0)          # 1% service fee
    method       = db.Column(db.String(30), default='vnpay')    # vnpay|momo|stripe
    status       = db.Column(db.String(20), default='pending')  # pending|success|failed
    txn_ref      = db.Column(db.String(100), unique=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def amount_formatted(self):
        return f"{self.amount:,} đ".replace(",", ".")

    @property
    def fee_formatted(self):
        return f"{self.fee:,} đ".replace(",", ".")
