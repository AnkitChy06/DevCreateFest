from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import timedelta
import os
from dotenv import load_dotenv
import logging
from .extensions import db

# Load environment variables
load_dotenv()

# Initialize Flask extensions
bcrypt = Bcrypt()
jwt = JWTManager()
compress = Compress()

# Import blueprints
from .routes.auth import auth_bp
from .routes.api.eco_routes import eco_bp
from .routes.api.learning_routes import learning_bp
from .routes.api.social_routes import social_bp
from .routes.api.analytics_routes import analytics_bp

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "instance", "arvora.db")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'jwt-secret-key'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
        JWT_COOKIE_SECURE=True,
        JWT_COOKIE_CSRF_PROTECT=True
    )
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    compress.init_app(app)
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Configure CORS with strict settings
    CORS(app, 
         resources={r"/api/*": {"origins": os.getenv('ALLOWED_ORIGINS', '*').split(',')},
                   r"/static/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         expose_headers=["Content-Range", "X-Total-Count"],
         supports_credentials=True
    )
    
    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        response.headers.update({
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'SAMEORIGIN',
            'X-XSS-Protection': '1; mode=block',
            'Content-Security-Policy': "default-src 'self'"
        })
        return response

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