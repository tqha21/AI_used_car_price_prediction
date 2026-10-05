from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.vehicle import Vehicle, Notification
from ml.predictor import predict_price
from extensions import db
import os, uuid
try:
    from PIL import Image
    from io import BytesIO
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from controllers.upload_controller import allowed_file, get_upload_dir, MAX_SIZE_MB

sell_bp = Blueprint('sell', __name__)


@sell_bp.route('/ban-xe', methods=['GET', 'POST'])
@login_required
def sell():
    """Trang đăng tin bán xe"""
    brands = Vehicle.get_brands()

    # Default form data
    form_data = {
        'brand': 'Mercedes-Benz',
        'model': 'C-Class',
        'year': 2022,
        'mileage': 22500,
        'description': '',
        'price': '',
        'fuel_type': 'Xăng',
        'transmission': 'Tự động',
        'color': 'Trắng',
        'version': '',
    }

    if request.method == 'POST':
        action = request.form.get('action', 'post')

        # Read form fields
        form_data['brand']        = request.form.get('brand', form_data['brand'])
        form_data['model']        = request.form.get('model', form_data['model'])
        form_data['year']         = int(request.form.get('year', form_data['year']))
        
        raw_mileage = request.form.get('mileage', str(form_data['mileage']))
        if isinstance(raw_mileage, str):
            raw_mileage = raw_mileage.replace(',', '').replace('.', '')
        form_data['mileage'] = int(raw_mileage) if raw_mileage else 0
        
        form_data['description']  = request.form.get('description', '')
        
        raw_price = request.form.get('price', '')
        if isinstance(raw_price, str):
            raw_price = raw_price.replace(',', '').replace('.', '')
        form_data['price'] = raw_price
        
        form_data['fuel_type']    = request.form.get('fuel', 'Xăng')
        form_data['transmission'] = request.form.get('transmission', 'Tự động')
        form_data['color']        = request.form.get('color', 'Trắng')
        form_data['version']      = request.form.get('version', '')

        if action in ('post', 'draft'):
            # ── Image upload ──────────────────────────────────────
            uploaded_urls = []
            files = request.files.getlist('images')
            for f in files:
                if f and f.filename and allowed_file(f.filename):
                    content = f.read()
                    if len(content) > MAX_SIZE_MB * 1024 * 1024:
                        continue
                    ext = f.filename.rsplit('.', 1)[1].lower()
                    filename = f"{uuid.uuid4().hex}.{ext}"
                    save_path = os.path.join(get_upload_dir(), filename)
                    try:
                        if PIL_AVAILABLE:
                            img = Image.open(BytesIO(content)).convert('RGB')
                            if img.width > 1200:
                                ratio = 1200 / img.width
                                img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
                            img.save(save_path, quality=85, optimize=True)
                        else:
                            with open(save_path, 'wb') as fp:
                                fp.write(content)
                        uploaded_urls.append(f"/static/uploads/{filename}")
                    except Exception:
                        pass

            if not uploaded_urls:
                uploaded_urls = ["https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&q=80"]

            # ── AI price suggestion ───────────────────────────────
            ai_price = 0
            try:
                suggestion = predict_price(
                    form_data['brand'], form_data['model'],
                    form_data['year'], form_data['mileage']
                )
                ai_price = suggestion.get('price', 0)
            except Exception:
                pass

            final_price  = int(form_data['price'] or ai_price or 1_000_000_000)
            final_status = 'draft' if action == 'draft' else 'pending'

            v = Vehicle(
                user_id      = current_user.id,
                brand        = form_data['brand'],
                model        = form_data['model'],
                year         = form_data['year'],
                mileage      = form_data['mileage'],
                fuel_type    = form_data['fuel_type'],
                transmission = form_data['transmission'],
                color        = form_data['color'],
                description  = form_data['description'],
                price        = final_price,
                ai_price     = ai_price or final_price,
                images       = ','.join(uploaded_urls),
                status       = final_status,
            )
            db.session.add(v)

            # ── Notifications ─────────────────────────────────────
            from extensions import socketio
            if final_status == 'draft':
                notif = Notification(
                    user_id=current_user.id,
                    title='📝 Đã lưu bản nháp',
                    message=f'Tin đăng xe {v.brand} {v.model} đã được lưu vào bản nháp.',
                    notif_type='info'
                )
                db.session.add(notif)
                db.session.commit()
                flash('📝 Tin đăng đã được lưu vào bản nháp!', 'success')
            else:
                from models.user import User
                admin = User.query.filter_by(role='admin').first()
                admin_id = admin.id if admin else current_user.id
                
                admin_notif = Notification(
                    user_id=admin_id,
                    title='🔔 Có tin đăng mới!',
                    message=f"Xe {v.brand} {v.model} đang chờ duyệt.",
                    notif_type='info'
                )
                seller_notif = Notification(
                    user_id=current_user.id,
                    title='✅ Đăng tin thành công',
                    message='Tin đăng của bạn đang được kiểm duyệt. Chúng tôi sẽ phê duyệt trong 2–4 giờ.',
                    notif_type='success'
                )
                db.session.add_all([admin_notif, seller_notif])
                db.session.commit()

                try:
                    socketio.emit('new_notification',
                        {'title': admin_notif.title, 'message': admin_notif.message, 'type': 'info'},
                        room=f'user_{admin_id}')
                    socketio.emit('new_notification',
                        {'title': seller_notif.title, 'message': seller_notif.message, 'type': 'success'},
                        room=f'user_{current_user.id}')
                except Exception:
                    pass

                flash('✅ Tin đăng đã gửi thành công và đang chờ duyệt!', 'success')

            return redirect(url_for('profile.profile'))

    # ── GET: prefetch AI suggestion ───────────────────────────
    ai_suggestion = None
    try:
        ai_suggestion = predict_price(
            form_data['brand'], form_data['model'],
            form_data['year'], form_data['mileage']
        )
        # Add formatted high/low
        if ai_suggestion:
            p = ai_suggestion['price']
            ai_suggestion['price_low_formatted']  = f"{int(p * 0.92):,} đ".replace(',', '.')
            ai_suggestion['price_high_formatted'] = f"{int(p * 1.10):,} đ".replace(',', '.')
    except Exception:
        pass

    models = Vehicle.get_models_by_brand(form_data['brand'])

    return render_template('sell.html',
        active_nav    = 'ban_xe',
        brands        = brands,
        models        = models,
        form_data     = form_data,
        ai_suggestion = ai_suggestion,
    )


@sell_bp.route('/api/sell/ai-description', methods=['POST'])
@login_required
def ai_description():
    """Sinh mô tả xe tự động dựa trên thông tin form"""
    data  = request.get_json(force=True)
    brand = data.get('brand', '')
    model = data.get('model', '')
    year  = data.get('year', 2022)
    mileage = int(data.get('mileage', 30000))
    color = data.get('color', '')

    desc = (
        f"Cần Chuyển Nhượng: {brand} {model} (Model {year}) – "
        f"Ngoại thất {color}, nội thất da cao cấp.\n\n"
        f"• Xe chính chủ từ đầu, cam kết không tai nạn, không ngập nước.\n"
        f"• ODO thực tế {mileage:,} km, đầy đủ lịch sử bảo dưỡng chính hãng.\n"
        f"• Pháp lý hoàn toàn sạch, sẵn sàng sang tên ngay.\n\n"
        f"Liên hệ để xem xe thực tế và kiểm định miễn phí bởi LuxDrive AI."
    ).replace(',', '.')

    return jsonify({'description': desc})


@sell_bp.route('/api/sell/similar-listings')
def similar_listings():
    """Đếm số xe tương tự đang niêm yết"""
    brand = request.args.get('brand', '')
    model = request.args.get('model', '')
    count = Vehicle.query.filter_by(brand=brand, status='live').count()
    return jsonify({'count': count, 'brand': brand, 'model': model})
