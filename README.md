# 🚗 Luxdrive - AI Used Car Price Prediction & Marketplace

Luxdrive là một nền tảng thương mại điện tử chuyên biệt dành cho thị trường xe ô tô cũ, kết hợp với sức mạnh của **Trí tuệ nhân tạo (AI)** để dự đoán và gợi ý giá xe một cách minh bạch, công bằng.

## 🌟 Tính năng nổi bật

- **Dự đoán giá xe bằng AI (AI Price Prediction):** Hệ thống tích hợp mô hình Machine Learning (Random Forest/XGBoost) để đánh giá và đưa ra mức giá hợp lý nhất dựa trên thông số kỹ thuật và tình trạng thực tế của xe.
- **Thị trường mua bán xe:** Nền tảng cho phép người dùng đăng tin bán xe, duyệt tìm xe theo nhu cầu (Hãng, dòng xe, năm sản xuất, giá cả).
- **Hệ thống thanh toán:** Tích hợp giao dịch an toàn qua cổng thanh toán trực tuyến (VNPAY).
- **Thông báo thời gian thực:** Cập nhật ngay lập tức các trạng thái giao dịch, thay đổi về giá hoặc tin nhắn thông qua hệ thống Notification.
- **Quản lý người dùng & VIP:** Phân quyền người dùng mua/bán và hệ thống cấp độ thành viên (VIP) với nhiều ưu đãi.

## 🏗️ Kiến trúc hệ thống

Dự án được xây dựng theo kiến trúc hiện đại, tách biệt rõ ràng giữa các phân hệ:
1. **Frontend:** Giao diện người dùng trực quan trên nền tảng Web/Mobile.
2. **Backend API:** Cung cấp RESTful API để xử lý nghiệp vụ (User, Vehicle, Transaction, Notification).
3. **AI Service:** Một service độc lập bằng Python (FastAPI/Flask) chạy mô hình Machine Learning dự đoán giá xe.
4. **Database:** Sử dụng MySQL cho dữ liệu quan hệ (`luxdrive.sql`).

## ⚙️ Cài đặt & Khởi chạy

### Yêu cầu hệ thống
- Database: MySQL
- Backend Environment (Node.js / Python)
- Phân hệ AI: Python 3.8+, Scikit-learn, FastAPI / Flask

### Hướng dẫn cài đặt
1. **Clone repository:**
   ```bash
   git clone https://github.com/tqha21/AI_used_car_price_prediction.git
   cd AI_used_car_price_prediction
   ```

2. **Khởi tạo Cơ sở dữ liệu:**
   - Tạo database `luxdrive` trong MySQL.
   - Import file `luxdrive/luxdrive.sql` để khởi tạo các bảng (users, vehicles, transactions, notifications).

*(Bổ sung hướng dẫn chi tiết để cài đặt Dependencies và chạy Backend, Frontend và AI Service tại đây)*

## 📊 Cơ sở dữ liệu (Database Schema)
Bao gồm 4 bảng chính:
- `users`: Quản lý tài khoản (vai trò, VIP, hash password).
- `vehicles`: Lưu trữ thông tin xe đăng bán và giá AI dự đoán (`ai_price`).
- `transactions`: Ghi nhận lịch sử giao dịch thanh toán.
- `notifications`: Hệ thống thông báo gửi đến người dùng.

## 🚀 Hướng phát triển tương lai
- Thu thập thêm dữ liệu thị trường thực tế tại Việt Nam để nâng cao độ chính xác của AI.
- Tích hợp Computer Vision để đánh giá tình trạng ngoại thất xe thông qua hình ảnh.
- Tích hợp thêm các phương thức thanh toán và dịch vụ kiểm định xe độc lập.

---
**Tác giả:** [tqha21](https://github.com/tqha21)
