import secrets
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt
from models.user import User
from models.vehicle import Notification

auth_bp = Blueprint('auth', __name__)

# ── DECORATORS ────────────────────────────────────────────
from functools import wraps
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('⛔ Bạn không có quyền truy cập trang này.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def seller_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role not in ('admin', 'seller'):
            flash('⚠️ Chức năng này chỉ dành cho người bán.', 'warning')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated

# ── ROUTES ────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    error = None
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'✅ Chào mừng trở lại, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        error = 'Email hoặc mật khẩu không chính xác.'
    return render_template('auth/login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    error = None
    form   = {}
    if request.method == 'POST':
        form = {k: request.form.get(k, '').strip() for k in
                ('first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password', 'role')}
        full_name = f"{form['last_name']} {form['first_name']}".strip()
        if not full_name:
            error = 'Vui lòng nhập đầy đủ họ và tên.'
        elif not form['email'] or '@' not in form['email']:
            error = 'Email không hợp lệ.'
        elif User.query.filter_by(email=form['email'].lower()).first():
            error = 'Email này đã được đăng ký.'
        elif len(form['password']) < 6:
            error = 'Mật khẩu ít nhất 6 ký tự.'
        elif form['password'] != form['confirm_password']:
            error = 'Mật khẩu xác nhận không khớp.'
        
        if not error:
            role = 'seller' if form['role'] == 'seller' else 'buyer'
            user = User(
                full_name=full_name,
                email=form['email'].lower(),
                phone=form['phone'],
                role=role,
                is_vip=(role == 'seller')
            )
            user.set_password(form['password'])
            db.session.add(user)
            # Welcome notification
            db.session.flush()
            notif = Notification(
                user_id=user.id,
                title='Chào mừng đến với LuxDrive AI! 🎉',
                message=f'Xin chào {user.full_name}, tài khoản của bạn đã được tạo thành công.',
                notif_type='success'
            )
            db.session.add(notif)
            db.session.commit()
            login_user(user)
            flash('✅ Đăng ký thành công!', 'success')
            return redirect(url_for('main.index'))
    return render_template('auth/register.html', error=error, form=form)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    sent = False
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user  = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            db.session.commit()
            # In production: send email with reset link
            # reset_link = url_for('auth.reset_password', token=token, _external=True)
        sent = True  # Always show "sent" to prevent email enumeration
    return render_template('auth/forgot_password.html', sent=sent)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('👋 Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('main.index'))
