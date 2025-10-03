from app.models import db
from datetime import datetime

class LearningPath(db.Model):
    __tablename__ = 'learning_paths'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20))  # 'beginner', 'intermediate', 'advanced'
    prerequisites = db.Column(db.JSON)
    total_points = db.Column(db.Integer, default=0)
    estimated_hours = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    modules = db.relationship('LearningModule', back_populates='path')

class LearningModule(db.Model):
    __tablename__ = 'learning_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey('learning_paths.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    content_type = db.Column(db.String(50))  # 'video', 'article', 'quiz', etc.
    content = db.Column(db.JSON)  # Stores module content or external links
    points = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer)  # For sequencing modules
    
    # Relationships
    path = db.relationship('LearningPath', back_populates='modules')
    completions = db.relationship('ModuleCompletion', back_populates='module')

class ModuleCompletion(db.Model):
    __tablename__ = 'module_completions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('learning_modules.id'))
    score = db.Column(db.Float)  # For quizzes/assessments
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='completed_modules')
    module = db.relationship('LearningModule', back_populates='completions')