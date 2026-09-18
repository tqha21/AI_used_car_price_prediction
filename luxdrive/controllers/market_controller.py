from flask import Blueprint, render_template
from models.market import MarketRepository

market_bp = Blueprint('market', __name__)

@market_bp.route('/thi-truong')
def market():
    """Trang thông tin thị trường"""
    kpis = MarketRepository.get_kpis()
    brand_bars = MarketRepository.get_brand_retention()
    chart_points = MarketRepository.get_chart_points()
    # Tính toán SVG path cho chart
    max_val = max(p.value for p in chart_points)
    min_val = min(p.value for p in chart_points)
    chart_h = 180
    chart_w = 500
    n = len(chart_points)
    points = []
    for i, p in enumerate(chart_points):
        x = (i / (n - 1)) * chart_w
        y = chart_h - ((p.value - min_val) / (max_val - min_val + 0.001)) * (chart_h - 20) - 10
        points.append((x, y))
    svg_path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return render_template('market.html',
        active_nav='thi_truong',
        kpis=kpis,
        brand_bars=brand_bars,
        chart_points=chart_points,
        svg_path=svg_path
    )
