from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.eco_calculator import log_eco_action, get_user_impact, create_community_project
from app.utils.achievement_handler import get_user_achievements
from app.utils.auth_validator import validate_user_exists
from app.utils.helpers import validate_data, paginate_query

eco_bp = Blueprint('eco', __name__)

@eco_bp.route('/actions', methods=['POST'])
@jwt_required()
def log_action():
    """Record an eco-friendly action"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not validate_data(data, ['action_id', 'quantity'])[0]:
        return jsonify({'error': 'Missing required fields'}), 400
    
    impact = log_eco_action(user_id, data['action_id'], data.get('quantity', 1))
    if impact is None:
        return jsonify({'error': 'Invalid action ID'}), 400
    
    return jsonify({
        'success': True,
        'impact': impact,
        'message': 'Action recorded successfully'
    }), 201

@eco_bp.route('/impact', methods=['GET'])
@jwt_required()
def get_impact():
    """Get user's environmental impact"""
    user_id = get_jwt_identity()
    impact_data = get_user_impact(user_id)
    
    if impact_data is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(impact_data), 200

@eco_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new community project"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not validate_data(data, ['name', 'description', 'goal'])[0]:
        return jsonify({'error': 'Missing required fields'}), 400
    
    project = create_community_project(
        name=data['name'],
        description=data['description'],
        goal=float(data['goal']),
        creator_id=user_id
    )
    
    return jsonify({
        'success': True,
        'project_id': project.id,
        'message': 'Project created successfully'
    }), 201

@eco_bp.route('/achievements', methods=['GET'])
@jwt_required()
def achievements():
    """Get user's eco achievements"""
    user_id = get_jwt_identity()
    achievements = get_user_achievements(user_id)
    
    return jsonify({
        'achievements': achievements
    }), 200