from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from flask_migrate import Migrate
from datetime import timedelta
import os
from dotenv import load_dotenv
import logging
from .models import db
from .routes.auth import auth_bp
from .routes.api.eco_routes import eco_bp
from .routes.api.learning_routes import learning_bp
from .routes.api.social_routes import social_bp
from .routes.api.analytics_routes import analytics_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Configure CORS with stricter settings
    CORS(app, 
         resources={r"/api/*": {"origins": os.getenv('ALLOWED_ORIGINS', '*').split(',')},
                   r"/static/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         expose_headers=["Content-Range", "X-Total-Count"],
         supports_credentials=True
    )
    
    # Configure rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Enable compression
    Compress(app)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arvora.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure JWT with enhanced security
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Shorter token expiry
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_COOKIE_SECURE'] = True
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    jwt = JWTManager(app)
    
    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints with rate limits
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    limiter.limit("5 per minute")(auth_bp)
    
    app.register_blueprint(eco_bp, url_prefix='/api/eco')
    app.register_blueprint(learning_bp, url_prefix='/api/learning')
    app.register_blueprint(social_bp, url_prefix='/api/social')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    
    # Keep existing routes for backward compatibility
    from .routes.legacy import register_legacy_routes
    register_legacy_routes(app)
    
    # Basic error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal Server Error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app