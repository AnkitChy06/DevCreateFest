from flask_jwt_extended import create_access_token
from datetime import timedelta
from ..models.user import User
from ..models import db
import random
import string

def generate_referral_code():
    """Generate a unique 6-character referral code"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not User.query.filter_by(referral_code=code).first():
            return code

class AuthService:
    @staticmethod
    def register(data):
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already registered'}, 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            school_id=data.get('school_id'),
            referral_code=generate_referral_code()
        )
        user.set_password(data['password'])
        
        # Handle referral
        if 'referral_code' in data:
            referrer = User.query.filter_by(referral_code=data['referral_code']).first()
            if referrer:
                user.referred_by = referrer.id
                referrer.eco_points += 100  # Bonus points for successful referral
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role},
            expires_delta=timedelta(days=1)
        )
        
        return {
            'token': token,
            'user': user.to_dict()
        }, 201
    
    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return {'error': 'Invalid email or password'}, 401
        
        token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role},
            expires_delta=timedelta(days=1)
        )
        
        return {
            'token': token,
            'user': user.to_dict()
        }, 200