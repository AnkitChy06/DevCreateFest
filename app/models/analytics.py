from app.models import db
from datetime import datetime

class UserAnalytics(db.Model):
    __tablename__ = 'user_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    login_count = db.Column(db.Integer, default=0)
    challenges_completed = db.Column(db.Integer, default=0)
    points_earned = db.Column(db.Integer, default=0)
    lessons_completed = db.Column(db.Integer, default=0)
    time_spent_minutes = db.Column(db.Integer, default=0)
    eco_impact = db.Column(db.JSON)  # Stores environmental impact metrics
    
    user = db.relationship('User', backref='analytics')

class SchoolAnalytics(db.Model):
    __tablename__ = 'school_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    date = db.Column(db.Date)
    active_students = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    challenges_completed = db.Column(db.Integer, default=0)
    eco_impact = db.Column(db.JSON)
    top_performers = db.Column(db.JSON)  # Stores top student IDs and scores
    
    school = db.relationship('School', backref='analytics')