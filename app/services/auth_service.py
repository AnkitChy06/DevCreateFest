from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime
from ..models.user import User
from ..models import db
from .. import bcrypt
from ..utils.error_handlers import APIError
import random
import string

def generate_referral_code():
    """Generate a unique 6-character referral code"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not User.query.filter_by(referral_code=code).first():
            return code

def update_user_streak(user):
    now = datetime.utcnow()
    
    if not user.last_streak_date:
        user.streak = 1
    else:
        days_diff = (now - user.last_streak_date).days
        if days_diff == 1:
            user.streak += 1
        elif days_diff > 1:
            user.streak = 1
    
    user.last_streak_date = now
    db.session.commit()

class AuthService:
    @staticmethod
    def register_user(data):
        if User.query.filter_by(email=data['email'].lower()).first():
            raise APIError('Email already registered', status_code=400)
        
        user = User(
            name=data['name'],
            email=data['email'].lower(),
            role=data.get('role', 'student')
        )
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.referral_code = generate_referral_code()
        
        if 'referral_code' in data:
            referrer = User.query.filter_by(referral_code=data['referral_code']).first()
            if referrer:
                user.referred_by = referrer.id
                referrer.eco_points += 50
        
        try:
            db.session.add(user)
            db.session.commit()
            
            token = create_access_token(
                identity=user.id,
                additional_claims={'role': user.role},
                expires_delta=timedelta(days=1)
            )
            
            return {
                'token': token,
                'user': user.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            raise APIError('Error creating user', status_code=500) from e

    @staticmethod
    def login_user(data):
        user = User.query.filter_by(email=data['email'].lower()).first()
        
        if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
            raise APIError('Invalid email or password', status_code=401)
        
        update_user_streak(user)
        
        token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role},
            expires_delta=timedelta(days=1)
        )
        
        return {
            'token': token,
            'user': user.to_dict()
        }