from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.analytics_helper import (
    update_user_analytics, update_school_analytics,
    get_user_statistics, get_school_statistics
)
from app.utils.auth_validator import admin_required, teacher_required
from app.utils.helpers import validate_data, paginate_query

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
@teacher_required()
def get_user_analytics(user_id):
    """Get analytics for a specific user"""
    update_user_analytics(user_id)  # Refresh analytics
    stats = get_user_statistics(user_id)
    
    if stats is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(stats), 200

@analytics_bp.route('/school/<int:school_id>', methods=['GET'])
@jwt_required()
@admin_required()
def get_school_analytics(school_id):
    """Get analytics for a specific school"""
    update_school_analytics(school_id)  # Refresh analytics
    stats = get_school_statistics(school_id)
    
    if stats is None:
        return jsonify({'error': 'School not found'}), 404
    
    return jsonify(stats), 200

@analytics_bp.route('/update/user/<int:user_id>', methods=['POST'])
@jwt_required()
@teacher_required()
def trigger_user_analytics_update(user_id):
    """Manually trigger analytics update for a user"""
    if update_user_analytics(user_id):
        return jsonify({
            'success': True,
            'message': 'User analytics updated successfully'
        }), 200
    
    return jsonify({
        'error': 'Failed to update user analytics'
    }), 400

@analytics_bp.route('/update/school/<int:school_id>', methods=['POST'])
@jwt_required()
@admin_required()
def trigger_school_analytics_update(school_id):
    """Manually trigger analytics update for a school"""
    if update_school_analytics(school_id):
        return jsonify({
            'success': True,
            'message': 'School analytics updated successfully'
        }), 200
    
    return jsonify({
        'error': 'Failed to update school analytics'
    }), 400