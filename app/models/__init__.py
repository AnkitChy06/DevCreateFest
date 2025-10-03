from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models in order of dependencies
    from . import school  # Base model without dependencies
    from . import user   # Depends on school
    
    # Rest of the models that may depend on school and user
    from . import (
        challenge,
        lesson,
        badge,
        gamification,
        achievement,
        analytics,
        eco_impact,
        learning,
        social
    )
    
    with app.app_context():
        db.create_all()