from . import db
from datetime import datetime

class School(db.Model):
    __tablename__ = 'schools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', backref='school')
    teachers = db.relationship('User', 
                             primaryjoin="and_(User.school_id==School.id, User.role=='teacher')",
                             backref='teaching_school')