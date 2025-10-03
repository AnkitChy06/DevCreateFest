from app.models import db
from datetime import datetime
import json

class Achievement(db.Model):
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(255))
    points = db.Column(db.Integer, default=0)
    requirements = db.Column(db.JSON)  # Stores achievement criteria
    category = db.Column(db.String(50))  # e.g., 'learning', 'eco', 'social'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'))
    progress = db.Column(db.JSON)  # Stores progress towards achievement
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    shared = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='achievements_earned')
    achievement = db.relationship('Achievement')