from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    return jsonify(challenges)

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    # Sort by points descending, take top 10
    top_users = sorted(users, key=lambda u: u['points'], reverse=True)[:10]
    return jsonify(top_users)

@app.route('/api/approvals', methods=['GET'])
def get_approvals():
    # Return only pending approvals
    pending_approvals = [app for app in approvals if app['status'] == 'Pending']
    return jsonify(pending_approvals)

@app.route('/api/user/<int:user_id>/complete-challenge', methods=['POST'])
def complete_challenge(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    challenge_id = data.get('challenge_id')
    challenge = next((c for c in challenges if c['id'] == challenge_id), None)
    
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
        
    user['points'] += challenge['points_reward']
    user['challenges_completed'] += 1
    
    if user['challenges_completed'] % 5 == 0:  # Level up every 5 challenges
        user['level'] += 1
        
    return jsonify({
        'success': True,
        'user': user,
        'points_earned': challenge['points_reward']
    })

@app.route('/api/challenge/accept/<int:challenge_id>', methods=['POST'])
def accept_challenge(challenge_id):
    challenge = next((c for c in challenges if c['id'] == challenge_id), None)
    if challenge:
        return jsonify({
            "message": "Challenge accepted!",
            "challenge_title": challenge['title']
        })
    return jsonify({"error": "Challenge not found"}), 404

@app.route('/api/approval/approve/<int:approval_id>', methods=['POST'])
def approve_item(approval_id):
    approval = next((a for a in approvals if a['id'] == approval_id), None)
    if approval:
        approval['status'] = 'Approved'
        return jsonify({
            "message": "Approval successful!",
            "updated_status": approval['status']
        })
    return jsonify({"error": "Approval not found"}), 404
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Simulated data structures (in-memory "database")
# User Data
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
    },
    {
        "id": 4,
        "name": "Bob Wilson",
        "level": 2,
        "points": 500,
        "challenges_completed": 5
    },
    {
        "id": 5,
        "name": "Carol Davis",
        "level": 4,
        "points": 900,
        "challenges_completed": 9
    },
    {
        "id": 6,
        "name": "David Brown",
        "level": 6,
        "points": 1200,
        "challenges_completed": 12
    },
    { "id": 7,
        "name": "Eve Garcia",
        "level": 1,
        "points": 200,
        "challenges_completed": 2
    },
    {
        "id": 8,
        "name": "Frank Miller",
        "level": 8,
        "points": 1800,
        "challenges_completed": 18
    },
    {
        "id": 9,
        "name": "Grace Lee",
        "level": 3,
        "points": 600,
        "challenges_completed": 6
    },
    {
        "id": 10,
        "name": "Henry Taylor",
        "level": 5,
        "points": 1100,
        "challenges_completed": 11
    },
      {
        "id": 11,
        "name": "Ivy Anderson",
        "level": 4,
        "points": 800,
        "challenges_completed": 8
    }
]
# Challenge Data
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
    },
    {"id": 3,
        "title": "Volunteer Time",
        "description": "Spend 30 minutes helping in the community",
        "points_reward": 75,
        "category": "Community"
    },
    {
        "id": 4,
        "title": "Exercise Routine",
        "description": "Complete a 20-minute workout",
        "points_reward": 40,
        "category": "Health"
    },
    {
        "id": 5,
        "title": "Learn a New Skill",
        "description": "Watch and practice a 15-minute tutorial",
        "points_reward": 60,
        "category": "Learning"
    }
]
# Approval Data (Pending items)
approvals = [
 {
        "id": 1,
        "user_name": "John Doe",
        "submission_details": "Submitted proof for Daily Meditation challenge",
        "status": "Pending"
    },
    {
        "id": 2,
        "user_name": "Jane Smith",
        "submission_details": "Submitted proof for Read a Book Chapter challenge",
        "status": "Pending"
    },
    {
        "id": 3,
        "user_name": "Alice Johnson",
        "submission_details": "Submitted proof for Volunteer Time challenge",
        "status": "Pending"
    }
]
# API Endpoints
@app.route('/api/profile', methods=['GET'])
def get_profile():
    # Simulate current user as the first in the list
    current_user = users[0]
    return jsonify(current_user)
@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    return jsonify(challenges)
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    # Sort by points descending, take top 10
    top_users = sorted(users, key=lambda u: u['points'], reverse=True)[:10]
    return jsonify(top_users)
@app.route('/api/approvals', methods=['GET'])
def get_approvals():
    # Return only pending approvals
    pending_approvals = [app for app in approvals if app['status'] == 'Pending']
    return jsonify(pending_approvals)
@app.route('/api/challenge/complete/<int:challenge_id>', methods=['POST'])
def complete_challenge(challenge_id):
    challenge = next((c for c in challenges if c['id'] == challenge_id), None)
    if challenge:
        # Update current user (first in list)
        current_user = users[0]
        current_user['points'] += challenge['points_reward']
        current_user['challenges_completed'] += 1
        return jsonify({
            "message": "Challenge completed successfully!",
            "points_earned": challenge['points_reward'],
            "new_points": current_user['points'],
            "new_completed": current_user['challenges_completed']
        })
    else:
        return jsonify({"error": "Challenge not found"}), 404
@app.route('/api/challenge/accept/<int:challenge_id>', methods=['POST'])
def accept_challenge(challenge_id):
    challenge = next((c for c in challenges if c['id'] == challenge_id), None)
    if challenge:
        # Simulate acceptance (no major data change, just confirmation)
        return jsonify({
            "message": "Challenge accepted!",
            "challenge_title": challenge['title']
        })
    else:
           return jsonify({"error": "Challenge not found"}), 404
@app.route('/api/approval/approve/<int:approval_id>', methods=['POST'])
def approve_item(approval_id):
    for approval in approvals:
        if approval['id'] == approval_id:
            approval['status'] = 'Approved'
            return jsonify({
                "message": "Approval successful!",
                "updated_status": approval['status']
            })
    return jsonify({"error": "Approval not found"}), 404
if __name__ == '__main__':
    app.run(debug=True)