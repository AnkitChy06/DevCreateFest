from flask import jsonify, request, make_response
from ..models import db
import logging

logger = logging.getLogger(__name__)

def register_legacy_routes(app):
    # Simulated data structures (in-memory "database")
    users = [
        {
            "id": 1,
            "name": "John Doe",
            "level": 5,
            "points": 1000,
            "challenges_completed": 10
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "level": 3,
            "points": 750,
            "challenges_completed": 7
        },
        {
            "id": 3,
            "name": "Alice Johnson",
            "level": 7,
            "points": 1500,
            "challenges_completed": 15
        }
    ]

    challenges = [
        {
            "id": 1,
            "title": "Daily Meditation",
            "description": "Meditate for 10 minutes every day",
            "points_reward": 25,
            "category": "Health"
        },
        {
            "id": 2,
            "title": "Read a Book Chapter",
            "description": "Read one chapter from a non-fiction book",
            "points_reward": 50,
            "category": "Learning"
        }
    ]

    def build_preflight_response():
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response

    def build_actual_response(response):
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/api/users', methods=['GET', 'OPTIONS'])
    def get_users():
        logger.debug('GET /api/users called')
        if request.method == 'OPTIONS':
            return build_preflight_response()
        return build_actual_response(jsonify(users))

    @app.route('/api/challenges', methods=['GET', 'OPTIONS'])
    def get_challenges():
        logger.debug('GET /api/challenges called')
        if request.method == 'OPTIONS':
            return build_preflight_response()
        return build_actual_response(jsonify(challenges))

    @app.route('/api/user/<int:user_id>', methods=['GET', 'OPTIONS'])
    def get_user(user_id):
        logger.debug(f'GET /api/user/{user_id} called')
        if request.method == 'OPTIONS':
            return build_preflight_response()
        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            return build_actual_response(jsonify(user))
        return build_actual_response(jsonify({'error': 'User not found'})), 404

    @app.route('/api/leaderboard', methods=['GET', 'OPTIONS'])
    def get_leaderboard():
        logger.debug('GET /api/leaderboard called')
        if request.method == 'OPTIONS':
            return build_preflight_response()
        top_users = sorted(users, key=lambda u: u['points'], reverse=True)[:10]
        return build_actual_response(jsonify(top_users))

    @app.route('/api/user/<int:user_id>/complete-challenge', methods=['POST', 'OPTIONS'])
    def complete_challenge(user_id):
        logger.debug(f'POST /api/user/{user_id}/complete-challenge called')
        if request.method == 'OPTIONS':
            return build_preflight_response()
            
        user = next((user for user in users if user['id'] == user_id), None)
        if not user:
            return build_actual_response(jsonify({'error': 'User not found'})), 404
        
        data = request.json
        challenge_id = data.get('challenge_id')
        challenge = next((c for c in challenges if c['id'] == challenge_id), None)
        
        if not challenge:
            return build_actual_response(jsonify({'error': 'Challenge not found'})), 404
            
        user['points'] += challenge['points_reward']
        user['challenges_completed'] += 1
        
        if user['challenges_completed'] % 5 == 0:  # Level up every 5 challenges
            user['level'] += 1
            
        return build_actual_response(jsonify({
            'success': True,
            'user': user,
            'points_earned': challenge['points_reward']
        }))

    @app.route('/')
    def index():
        return "API Server is running!"