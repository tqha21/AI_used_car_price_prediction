from datetime import datetime
from flask_login import UserMixin
from extensions import db, bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True)
    full_name   = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    phone       = db.Column(db.String(20))
    password_hash = db.Column(db.String(256), nullable=False)
    role        = db.Column(db.String(20), default='buyer')  # admin|seller|buyer
    avatar_url  = db.Column(db.String(300), default='https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=80&q=80')
    is_vip      = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    vehicles      = db.relationship('Vehicle', backref='owner', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    transactions  = db.relationship('Transaction', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def role_label(self):
        return {'admin': 'Quản trị viên', 'seller': 'Người bán VIP', 'buyer': 'Thành viên'}.get(self.role, self.role)

    @property
    def unread_notifications(self):
        return sum(1 for n in self.notifications if not n.is_read)
