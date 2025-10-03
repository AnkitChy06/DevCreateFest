from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    # Import all models to ensure they are registered
    from . import school, user, challenge, lesson, badge, gamification
    
    with app.app_context():
        db.create_all()