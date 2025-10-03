from . import db
from datetime import datetime
from .school import School
from .user import User

class EcoAction(db.Model):
    __tablename__ = 'eco_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    carbon_impact = db.Column(db.Float)  # CO2 savings in kg
    water_savings = db.Column(db.Float)  # Water savings in liters
    energy_savings = db.Column(db.Float)  # Energy savings in kWh
    points = db.Column(db.Integer, default=0)
    verification_type = db.Column(db.String(50))  # 'photo', 'gps', 'manual', etc.
    frequency = db.Column(db.String(20))  # 'daily', 'weekly', 'monthly'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserEcoAction(db.Model):
    __tablename__ = 'user_eco_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action_id = db.Column(db.Integer, db.ForeignKey('eco_actions.id'))
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    proof_url = db.Column(db.String(255))  # URL to verification photo/data
    location = db.Column(db.JSON)  # GPS coordinates if applicable
    impact_multiplier = db.Column(db.Float, default=1.0)  # For group actions
    verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', foreign_keys=[user_id], backref='eco_actions')
    action = db.relationship('EcoAction')
    verifier = db.relationship('User', foreign_keys=[verified_by])

class CommunityProject(db.Model):
    __tablename__ = 'community_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.JSON)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    target_impact = db.Column(db.JSON)  # Target environmental metrics
    actual_impact = db.Column(db.JSON)  # Achieved environmental metrics
    status = db.Column(db.String(20))  # 'planned', 'active', 'completed'
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='created_projects')
    school = db.relationship('School', backref='community_projects')
    participants = db.relationship('ProjectParticipant', back_populates='project')