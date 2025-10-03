from . import db
from datetime import datetime

class Challenge(db.Model):
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=0)
    type = db.Column(db.String(50))  # daily, weekly, special
    level = db.Column(db.Integer, default=1)
    media_required = db.Column(db.Boolean, default=False)
    teacher_approval_required = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    completions = db.relationship('UserChallengeCompletion', back_populates='challenge')

class UserChallengeCompletion(db.Model):
    __tablename__ = 'user_challenge_completions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    proof_url = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    points_awarded = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='completed_challenges',
                          foreign_keys=[user_id])
    challenge = db.relationship('Challenge', back_populates='completions')
    approver = db.relationship('User', foreign_keys=[approved_by])