from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.learning_tracker import (
    get_user_progress, mark_module_complete,
    get_recommended_modules, reset_module_progress
)
from app.utils.auth_validator import teacher_required
from app.utils.helpers import validate_data, paginate_query

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """Get user's learning progress"""
    user_id = get_jwt_identity()
    path_id = request.args.get('path_id', type=int)
    
    progress = get_user_progress(user_id, path_id)
    if progress is None:
        return jsonify({'error': 'Invalid path or user'}), 404
    
    return jsonify(progress), 200

@learning_bp.route('/modules/<int:module_id>/complete', methods=['POST'])
@jwt_required()
def complete_module(module_id):
    """Mark a module as completed"""
    user_id = get_jwt_identity()
    
    if mark_module_complete(user_id, module_id):
        return jsonify({
            'success': True,
            'message': 'Module marked as complete'
        }), 200
    
    return jsonify({
        'message': 'Module was already completed'
    }), 200

@learning_bp.route('/modules/recommended', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get recommended learning modules"""
    user_id = get_jwt_identity()
    recommendations = get_recommended_modules(user_id)
    
    if recommendations is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'recommendations': recommendations
    }), 200

@learning_bp.route('/modules/<int:module_id>/reset', methods=['POST'])
@jwt_required()
@teacher_required()
def reset_progress(module_id):
    """Reset a student's progress for a module"""
    data = request.get_json()
    if not validate_data(data, ['student_id'])[0]:
        return jsonify({'error': 'Student ID is required'}), 400
    
    if reset_module_progress(data['student_id'], module_id):
        return jsonify({
            'success': True,
            'message': 'Module progress reset successfully'
        }), 200
    
    return jsonify({
        'error': 'No completion record found'
    }), 404