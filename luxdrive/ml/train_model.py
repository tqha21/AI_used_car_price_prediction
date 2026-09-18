"""
LuxDrive AI - Train used car price prediction model with Advanced Gradient Boosting.
Run: python ml/train_model.py
Output: ml/car_price_model.pkl + ml/encoders.pkl
"""
import numpy as np
import joblib
import os
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

# Định nghĩa dữ liệu mô phỏng cao cấp
BRANDS_MODELS = {
    'Porsche': ['911 Carrera', 'Panamera', 'Macan', 'Cayenne', 'Taycan'],
    'Mercedes-Benz': ['S500', 'E300', 'C200', 'GLC 300', 'G63 AMG'],
    'BMW': ['X7', 'X5', '320i', '530i', '740i'],
    'Audi': ['Q8', 'Q7', 'A8', 'A6', 'RS e-tron GT'],
    'Ferrari': ['F8 Tributo', 'SF90 Stradale', 'Roma'],
    'Lamborghini': ['Urus', 'Huracan', 'Aventador'],
    'Lexus': ['LX600', 'RX350', 'ES250'],
    'Bentley': ['Flying Spur', 'Bentayga', 'Continental GT']
}
FUELS  = ['Xăng', 'Dầu', 'Hybrid', 'Điện']
TRANS  = ['Tự động', 'Số sàn', 'Ly hợp kép']

BASE_PRICES = {
    'Ferrari': 14_000_000_000, 'Lamborghini': 16_000_000_000,
    'Bentley': 10_000_000_000, 'Porsche': 4_500_000_000,  
    'Mercedes-Benz': 3_500_000_000, 'BMW': 3_000_000_000,
    'Audi': 2_800_000_000, 'Lexus': 2_500_000_000,
}

MODEL_MULTIPLIERS = {
    '911 Carrera': 1.8, 'G63 AMG': 2.5, 'Urus': 1.5, 'LX600': 1.8, 'X7': 1.6
}

def generate_data(n=20000):
    np.random.seed(42)
    rows = []
    brands = list(BRANDS_MODELS.keys())
    
    for _ in range(n):
        brand   = np.random.choice(brands)
        model   = np.random.choice(BRANDS_MODELS[brand])
        fuel    = np.random.choice(FUELS, p=[0.6, 0.2, 0.15, 0.05])
        trans   = np.random.choice(TRANS, p=[0.7, 0.1, 0.2])
        year    = np.random.randint(2010, 2025)
        mileage = np.random.randint(0, 150_000)
        
        base    = BASE_PRICES[brand] * MODEL_MULTIPLIERS.get(model, 1.0)
        
        # Công thức khấu hao chi tiết
        age_f   = max(0.4, 1 - (2024 - year) * 0.05)
        mile_f  = max(0.5, 1 - (mileage / 200_000) * 0.4)
        
        # Hệ số phụ
        fuel_bonus = 1.05 if fuel == 'Hybrid' else (1.1 if fuel == 'Điện' else 1.0)
        trans_bonus = 1.08 if trans == 'Ly hợp kép' else 1.0
        
        noise   = np.random.normal(1.0, 0.05) # Giảm noise để model fit tốt hơn
        price   = int(base * age_f * mile_f * fuel_bonus * trans_bonus * noise)
        rows.append([brand, model, year, mileage, trans, fuel, price])
        
    return pd.DataFrame(rows, columns=['Brand', 'Model', 'Year', 'Mileage', 'Transmission', 'Fuel', 'Price'])

def train():
    print("[LuxDrive ML] Đang tạo 20,000 dữ liệu mẫu phức tạp...")
    df = generate_data(20000)
    
    encoders = {}
    cat_cols = ['Brand', 'Model', 'Transmission', 'Fuel']
    
    # Label Encoding
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    X = df[['Brand', 'Model', 'Year', 'Mileage', 'Transmission', 'Fuel']]
    y = df['Price']
    
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    print("[LuxDrive ML] Bắt đầu huấn luyện GradientBoostingRegressor...")
    model = GradientBoostingRegressor(
        n_estimators=400, 
        max_depth=6,
        learning_rate=0.05, 
        subsample=0.8,
        min_samples_leaf=5,
        random_state=42
    )
    
    model.fit(X_tr, y_tr)
    preds = model.predict(X_te)
    
    mape = mean_absolute_percentage_error(y_te, preds) * 100
    rmse = np.sqrt(mean_squared_error(y_te, preds))
    
    print(f"[LuxDrive ML] Huấn luyện hoàn tất!")
    print(f"[LuxDrive ML] Đánh giá: MAPE = {mape:.2f}% | RMSE = {rmse:,.0f} đ")
    
    if mape > 15:
        print("[WARNING] MAPE quá cao, cân nhắc tối ưu thêm hyperparams.")

    os.makedirs('ml', exist_ok=True)
    joblib.dump(model, 'ml/car_price_model.pkl')
    joblib.dump(encoders, 'ml/encoders.pkl')
    print("[LuxDrive ML] Đã lưu: ml/car_price_model.pkl + ml/encoders.pkl")

if __name__ == '__main__':
    train()
