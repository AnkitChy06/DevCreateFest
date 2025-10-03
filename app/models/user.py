from . import db
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    avatar_url = db.Column(db.String(255))
    eco_points = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_streak_date = db.Column(db.DateTime)
    referral_code = db.Column(db.String(10), unique=True)
    referred_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), default='student')  # student, teacher, admin

    # Relationships
    badges = db.relationship('UserBadge', back_populates='user')
    completed_challenges = db.relationship('UserChallengeCompletion', back_populates='user')
    completed_lessons = db.relationship('UserProgress', back_populates='user')
    daily_streaks = db.relationship('UserStreak', back_populates='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf8')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'school_id': self.school_id,
            'avatar_url': self.avatar_url,
            'eco_points': self.eco_points,
            'streak': self.streak,
            'role': self.role
        }