from dataclasses import dataclass, field
from typing import List

@dataclass
class Dealer:
    name: str
    rating: float
    reviews: int
    address: str
    phone: str
    listings: int

@dataclass
class ListingDetail:
    id: int
    car_name: str
    brand: str
    year: int
    mileage: int
    fuel: str
    doors: int
    color: str
    price: int
    ai_price: int
    ai_confidence: int
    images: List[str]
    description: str
    features: List[str]
    dealer: Dealer

    @property
    def price_formatted(self):
        return f"{self.price:,} đ".replace(",", ".")

    @property
    def ai_price_billion(self):
        return f"{self.ai_price/1e9:.2f} Tỷ".replace(".", ",")

    @property
    def mileage_formatted(self):
        return f"{self.mileage:,} km".replace(",", ".")

    @property
    def price_diff_pct(self):
        diff = (self.price - self.ai_price) / self.ai_price * 100
        sign = "+" if diff >= 0 else ""
        return f"{sign}{diff:.1f}%"

    @property
    def price_diff_positive(self):
        return self.price >= self.ai_price

LISTINGS = {
    1: ListingDetail(
        id=1,
        car_name="Mercedes-Benz S450 Luxury 2023",
        brand="Mercedes-Benz", year=2023,
        mileage=12000, fuel="Xăng", doors=4, color="Đen",
        price=4_850_000_000, ai_price=4_900_000_000, ai_confidence=91,
        images=[
            "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80",
            "https://images.unsplash.com/photo-1549924231-f129b911e442?w=400&q=80",
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400&q=80",
            "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&q=80",
        ],
        description=(
            "Mercedes-Benz S450 Luxury năm 2023, màu đen bóng siêu sang trọng. "
            "Xe sử dụng kỹ lưỡng, bảo dưỡng đúng hạn tại đại lý chính hãng. "
            "Tình trạng nội ngoại thất như mới, không tai nạn ngập nước."
        ),
        features=[
            "Hệ thống âm thanh Burmester® 3D Surround",
            "Ghế massage 5 vùng trước sau",
            "Hệ thống treo khí AIRMATIC",
            "Màn hình MBUX Hyperscreen 56 inch",
            "Cửa sổ trời toàn cảnh Panoramic",
            "Cảm biến lùi + Camera 360°",
        ],
        dealer=Dealer(
            name="Salon LuxAuto ⭐",
            rating=4.8, reviews=127,
            address="135 Nguyễn Văn Linh, Quận 7, TP.HCM",
            phone="0901 234 567",
            listings=48
        )
    ),
    2: ListingDetail(
        id=2,
        car_name="Porsche 911 Carrera S 2021",
        brand="Porsche", year=2021,
        mileage=15000, fuel="Xăng", doors=2, color="Bạc",
        price=8_500_000_000, ai_price=8_200_000_000, ai_confidence=94,
        images=[
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80",
            "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=400&q=80",
            "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400&q=80",
            "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&q=80",
        ],
        description=(
            "Porsche 911 Carrera S đời 2021, bản Sport Chrono Package, màu bạc GT. "
            "Xe chính chủ, bảo dưỡng đúng hạn tại Porsche Centre Việt Nam. "
            "Hiệu suất vượt trội, tình trạng hoàn hảo."
        ),
        features=[
            "Sport Chrono Package",
            "Tự động PDK 8 cấp",
            "Hệ thống PASM Sport",
            "Phanh gốm Carbon (PCCB)",
            "Ghế thể thao 18 chiều chỉnh điện",
            "Bose Surround Sound System",
        ],
        dealer=Dealer(
            name="Prestige Auto Vietnam ⭐",
            rating=4.9, reviews=203,
            address="22 Lê Duẩn, Quận 1, TP.HCM",
            phone="0909 888 777",
            listings=31
        )
    ),
}

# ---- ADMIN DATA ----
@dataclass
class AdminStat:
    label: str
    value: str
    sub: str
    trend: str  # "up"|"down"|"neutral"

@dataclass
class PendingListing:
    id: int
    car: str
    seller: str
    price: str
    ai_price: str
    ai_pct: str
    ai_positive: bool
    date: str
    priority: str  # "High"|"Medium"|"Low"
    priority_color: str

ADMIN_STATS = [
    AdminStat("ACTIVE LISTINGS", "1,250", "Requires immediate action", "up"),
    AdminStat("PENDING MODERATION", "15",  "+6.8% this month", "down"),
    AdminStat("TOTAL REVENUE", "500tr VND", "+40.8% this bundle", "up"),
    AdminStat("AI CALLS", "5k",  "Sales performance", "neutral"),
]

PENDING_LISTINGS = [
    PendingListing(1, "Mercedes-Benz S450", "Nguyễn Thao", "4,85 Tỷ", "4,90 Tỷ", "+2.3%", True,  "24/10/2024", "High",   "#ef4444"),
    PendingListing(2, "Porsche Cayenne GTS", "Lê Minh",    "6,20 Tỷ", "5,85 Tỷ", "+5.9%", True,  "23/10/2024", "Medium", "#f59e0b"),
]
