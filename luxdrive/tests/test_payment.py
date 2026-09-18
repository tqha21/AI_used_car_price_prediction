import pytest
from app import create_app
from extensions import db
from models.user import User
from models.vehicle import Vehicle, Transaction

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Setup mock data
            user = User(full_name='Test User', email='test@luxdrive.ai', role='seller')
            user.set_password('123456')
            db.session.add(user)
            db.session.commit()
            
            vehicle = Vehicle(
                user_id=user.id, brand='Porsche', model='911', year=2021,
                mileage=10000, price=8000000000
            )
            db.session.add(vehicle)
            db.session.commit()
            
            yield client
            
        db.session.remove()
        db.drop_all()

def test_payment_escrow_transaction(client):
    """Test process payment creates escrow transaction and updates vehicle status"""
    with client.application.app_context():
        user = User.query.filter_by(email='test@luxdrive.ai').first()
        vehicle = Vehicle.query.first()
        
    # Login user
    client.post('/login', data={'email': 'test@luxdrive.ai', 'password': '123456'})
    
    # Process payment
    response = client.post(f'/payment/{vehicle.id}/process', data={'method': 'vnpay'})
    
    # Verify redirection to success page
    assert response.status_code == 302
    assert '/payment/success/' in response.location
    
    # Verify database state
    with client.application.app_context():
        txn = Transaction.query.filter_by(vehicle_id=vehicle.id).first()
        assert txn is not None
        assert txn.status == 'escrow_locked'
        assert txn.fee == int(vehicle.price * 0.01)
        
        v = Vehicle.query.get(vehicle.id)
        assert v.status == 'pending'
