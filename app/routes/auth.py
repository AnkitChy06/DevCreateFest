from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService
from ..utils.error_handlers import APIError
from ..utils.logger import setup_logger
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from ..models.user import User

auth_bp = Blueprint('auth', __name__)
logger = setup_logger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user with optional referral"""
    try:
        data = request.get_json()
        required_fields = ['name', 'email', 'password']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise APIError(f'Missing required field: {field}', status_code=400)
        
        # Register user
        result = AuthService.register_user(data)
        logger.info(f"New user registered: {data['email']}")
        
        return jsonify(result), 201
        
    except APIError as e:
        logger.warning(f"Registration failed: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise APIError('Internal server error', status_code=500) from e

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return token"""
    try:
        data = request.get_json()
        required_fields = ['email', 'password']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise APIError(f'Missing required field: {field}', status_code=400)
        
        # Authenticate user
        result = AuthService.login_user(data)
        logger.info(f"User logged in: {data['email']}")
        
        return jsonify(result)
        
    except APIError as e:
        logger.warning(f"Login failed: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise APIError('Internal server error', status_code=500) from e

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        from ..models.user import User
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500