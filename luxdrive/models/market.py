from dataclasses import dataclass
from typing import List

@dataclass
class KPI:
    label: str
    value: str
    change: str
    trend: str  # "up" | "down" | "neutral"

@dataclass
class BrandBar:
    name: str
    retention: int   # % giữ giá trị

@dataclass
class ChartPoint:
    month: str
    value: float

class MarketRepository:
    @staticmethod
    def get_kpis() -> List[KPI]:
        return [
            KPI("TỔNG SỐ GIAO DỊCH", "1,284", "+12.5%", "up"),
            KPI("GIÁ TRỊ XE TB", "3,5 Tỷ đ", "-2.1%", "down"),
            KPI("CHỈ SỐ BIẾN ĐỘNG THỊ TRƯỜNG", "42.8", "Ổn định", "neutral"),
        ]

    @staticmethod
    def get_brand_retention() -> List[BrandBar]:
        return [
            BrandBar("Porsche", 82),
            BrandBar("Mercedes", 65),
            BrandBar("BMW", 58),
            BrandBar("Audi", 52),
        ]

    @staticmethod
    def get_chart_points() -> List[ChartPoint]:
        return [
            ChartPoint("Thg 1", 2.8),
            ChartPoint("Thg 2", 2.6),
            ChartPoint("Thg 3", 2.9),
            ChartPoint("Thg 4", 3.1),
            ChartPoint("Thg 5", 3.4),
            ChartPoint("Thg 6", 3.5),
        ]
