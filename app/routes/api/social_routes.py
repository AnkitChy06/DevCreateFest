from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.social_manager import (
    create_connection, accept_connection, get_user_connections,
    remove_connection, get_user_notifications, mark_notification_read
)
from app.utils.helpers import validate_data, paginate_query

social_bp = Blueprint('social', __name__)

@social_bp.route('/connections', methods=['POST'])
@jwt_required()
def send_connection_request():
    """Send a connection request to another user"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not validate_data(data, ['friend_id'])[0]:
        return jsonify({'error': 'Friend ID is required'}), 400
    
    if create_connection(user_id, data['friend_id']):
        return jsonify({
            'success': True,
            'message': 'Connection request sent'
        }), 201
    
    return jsonify({
        'error': 'Connection already exists or invalid request'
    }), 400

@social_bp.route('/connections/accept', methods=['POST'])
@jwt_required()
def accept_request():
    """Accept a connection request"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not validate_data(data, ['friend_id'])[0]:
        return jsonify({'error': 'Friend ID is required'}), 400
    
    if accept_connection(user_id, data['friend_id']):
        return jsonify({
            'success': True,
            'message': 'Connection accepted'
        }), 200
    
    return jsonify({
        'error': 'No pending connection request found'
    }), 404

@social_bp.route('/connections', methods=['GET'])
@jwt_required()
def list_connections():
    """Get user's connections"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    
    connections = get_user_connections(user_id, status)
    return jsonify({
        'connections': connections
    }), 200

@social_bp.route('/connections/<int:friend_id>', methods=['DELETE'])
@jwt_required()
def delete_connection(friend_id):
    """Remove a connection"""
    user_id = get_jwt_identity()
    
    if remove_connection(user_id, friend_id):
        return jsonify({
            'success': True,
            'message': 'Connection removed'
        }), 200
    
    return jsonify({
        'error': 'Connection not found'
    }), 404

@social_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user's notifications"""
    user_id = get_jwt_identity()
    unread_only = request.args.get('unread', '').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    
    notifications = get_user_notifications(user_id, unread_only)
    items, total_pages, total = paginate_query(notifications, page)
    
    return jsonify({
        'notifications': items,
        'total_pages': total_pages,
        'total_items': total,
        'current_page': page
    }), 200

@social_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    """Mark a notification as read"""
    user_id = get_jwt_identity()
    
    if mark_notification_read(notification_id, user_id):
        return jsonify({
            'success': True,
            'message': 'Notification marked as read'
        }), 200
    
    return jsonify({
        'error': 'Notification not found'
    }), 404