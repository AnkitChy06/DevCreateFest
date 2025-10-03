from . import db
from datetime import datetime

class UserStreak(db.Model):
    __tablename__ = 'user_streaks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    streak_count = db.Column(db.Integer, default=0)
    last_completed_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='daily_streaks')

class Competition(db.Model):
    __tablename__ = 'competitions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('CompetitionParticipant', back_populates='competition')

class CompetitionParticipant(db.Model):
    __tablename__ = 'competition_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    points = db.Column(db.Integer, default=0)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    competition = db.relationship('Competition', back_populates='participants')
    user = db.relationship('User')