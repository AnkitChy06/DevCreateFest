from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from functools import wraps
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecoquest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Data Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    streak_days = db.Column(db.Integer, default=0)
    last_streak_date = db.Column(db.DateTime)
    avatar = db.Column(db.String(100), default='🧑‍🎓')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    level_required = db.Column(db.Integer, default=1)
    points_reward = db.Column(db.Integer, default=100)
    duration = db.Column(db.Integer, default=15)  # in minutes
    icon = db.Column(db.String(10), default='📚')

class UserLesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    score = db.Column(db.Integer, default=0)  # for quizzes

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    points_reward = db.Column(db.Integer, default=100)
    type = db.Column(db.String(20), default='general')  # daily, weekly, etc.
    icon = db.Column(db.String(10), default='🎯')
    is_active = db.Column(db.Boolean, default=True)

class UserChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    progress = db.Column(db.Float, default=0.0)  # 0-100%
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    submitted_evidence = db.Column(db.Text)  # e.g., photo URL or description

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(10), default='🏅')
    unlock_condition = db.Column(db.String(100))  # e.g., "complete 5 lessons", "streak 10 days"

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'badge_id', name='unique_user_badge'),)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)  # e.g., "95% score in course"
    icon = db.Column(db.String(10), default='📜')
    min_score = db.Column(db.Integer, default=90)  # percentage

class UserCertificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificate.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('user_id', 'certificate_id', name='unique_user_certificate'),)

# Decorator for authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # In production, validate JWT token; here, assume token is user_id for simplicity
            user_id = int(token.split(' ')[1]) if token.startswith('Bearer ') else int(token)
            current_user = User.query.get(user_id)
            if not current_user:
                return jsonify({'message': 'Token is invalid!'}), 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Helper function to update user level based on points
def update_user_level(user):
    # Simple level calculation: level = floor(points / 1000) + 1, min 1
    new_level = max(1, (user.points // 1000) + 1)
    if new_level > user.level:
        user.level = new_level
        # Could trigger level-up badge/certificate here

# Helper function to update streak
def update_streak(user):
    today = datetime.utcnow().date()
    if user.last_streak_date:
        last_date = user.last_streak_date.date()
        if today == last_date + timedelta(days=1):
            user.streak_days += 1
        elif today != last_date:
            user.streak_days = 1
    else:
        user.streak_days = 1
    user.last_streak_date = datetime.utcnow()

# Helper function to award badge if conditions met
def check_and_award_badges(user, context='general'):
    badges = Badge.query.all()
    for badge in badges:
        if not UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).first():
            # Simple condition checks (extend as needed)
            if badge.unlock_condition == 'complete 5 lessons' and UserLesson.query.filter_by(user_id=user.id, completed=True).count() >= 5:
                award_badge(user, badge)
            elif badge.unlock_condition == 'streak 10 days' and user.streak_days >= 10:
                award_badge(user, badge)
            elif badge.unlock_condition == 'first challenge' and context == 'first_challenge':
                award_badge(user, badge)
            # Add more conditions based on frontend (e.g., "10-day habit streak", "Perfect waste sorting")

def award_badge(user, badge):
    new_badge = UserBadge(user_id=user.id, badge_id=badge.id)
    db.session.add(new_badge)
    db.session.commit()
    # Bonus points for badge? user.points += 50; etc.

# Helper function to award certificate if conditions met
def check_and_award_certificates(user, score=None, context='general'):
    certificates = Certificate.query.all()
    for cert in certificates:
        if not UserCertificate.query.filter_by(user_id=user.id, certificate_id=cert.id).first():
            # Simple condition checks (extend as needed)
            if cert.name == 'Water Conservation Expert' and context == 'water_lesson' and score and score >= cert.min_score:
                award_certificate(user, cert, score)
            elif cert.name == 'Eco-Warrior Level 1' and user.challenges_completed >= 10 and user.streak_days >= 30:
                award_certificate(user, cert)
            # Add more based on frontend (e.g., "Completed 10 real-world challenges and maintained 30-day streak")

def award_certificate(user, cert, score=100):
    new_cert = UserCertificate(user_id=user.id, certificate_id=cert.id, score=score)
    db.session.add(new_cert)
    db.session.commit()
    # Bonus points? user.points += 200; etc.

# API Endpoints
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User  already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User  registered', 'user_id': new_user.id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        # In production, return JWT token; here, return user_id as token
        return jsonify({'message': 'Login successful', 'token': str(user.id)}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/user/<int:user_id>/dashboard', methods=['GET'])
@token_required
def get_dashboard(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    active_challenges = UserChallenge.query.filter_by(user_id=user_id, completed=False).count()
    completed_lessons = UserLesson.query.filter_by(user_id=user_id, completed=True).count()

    # Add user.challenges_completed as a computed field or query
    user.challenges_completed = UserChallenge.query.filter_by(user_id=user_id, completed=True).count()

    return jsonify({
        'user': {
            'username': user.username,
            'points': user.points,
            'level': user.level,
            'streak_days': user.streak_days,
            'avatar': user.avatar
        },
        'stats': {
            'active_challenges': active_challenges,
            'completed_lessons': completed_lessons,
            'challenges_completed': user.challenges_completed
        }
    })

@app.route('/api/lessons', methods=['GET'])
@token_required
def get_lessons(current_user):
    lessons = Lesson.query.filter_by().all()  # Filter by level if needed
    lesson_list = []
    for lesson in lessons:
        user_lesson = UserLesson.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
        lesson_list.append({
            'id': lesson.id,
            'title': lesson.title,
            'description': lesson.description,
            'level_required': lesson.level_required,
            'points_reward': lesson.points_reward,
            'duration': lesson.duration,
            'icon': lesson.icon,
            'completed': user_lesson.completed if user_lesson else False,
            'score': user_lesson.score if user_lesson else 0
        })
    return jsonify({'lessons': lesson_list})

@app.route('/api/lessons/<int:lesson_id>/complete', methods=['POST'])
@token_required
def complete_lesson(current_user, lesson_id):
    data = request.get_json()
    score = data.get('score', 100)  # Assume 100% if not provided

    lesson = Lesson.query.get(lesson_id)
    if not lesson or current_user.level < lesson.level_required:
        return jsonify({'message': 'Lesson not accessible'}), 400

    user_lesson = UserLesson.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    if not user_lesson:
        user_lesson = UserLesson(user_id=current_user.id, lesson_id=lesson_id)

    if score >= 90:  # Threshold for certificate
        check_and_award_certificates(current_user, score, 'water_lesson')  # Example for water lesson

    user_lesson.completed = True
    user_lesson.completed_at = datetime.utcnow()
    user_lesson.score = score
    current_user.points += lesson.points_reward
    update_user_level(current_user)
    check_and_award_badges(current_user, 'lesson_complete')

    db.session.commit()
    return jsonify({'message': 'Lesson completed', 'points_earned': lesson.points_reward})

@app.route('/api/challenges', methods=['GET'])
@token_required
def get_challenges(current_user):
    challenges = Challenge.query.filter_by(is_active=True).all()
    challenge_list = []
    for challenge in challenges:
        user_challenge = UserChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge.id).first()
        challenge_list.append({
            'id': challenge.id,
            'title': challenge.title,
            'description': challenge.description,
            'points_reward': challenge.points_reward,
            'type': challenge.type,
            'icon': challenge.icon,
            'progress': user_challenge.progress if user_challenge else 0,
            'completed': user_challenge.completed if user_challenge else False
        })
    return jsonify({'challenges': challenge_list})

@app.route('/api/challenges/<int:challenge_id>/progress', methods=['POST'])
@token_required
def update_challenge_progress(current_user, challenge_id):
    data = request.get_json()
    progress = data.get('progress', 0)  # 0-100

    challenge = Challenge.query.get(challenge_id)
    if not challenge:
        return jsonify({'message': 'Challenge not found'}), 404

    user_challenge = UserChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()
    if not user_challenge:
        user_challenge = UserChallenge(user_id=current_user.id, challenge_id=challenge_id)

    user_challenge.progress = min(100, max(0, progress))
    if user_challenge.progress >= 100:
        user_challenge.completed = True
        user_challenge.completed_at = datetime.utcnow()
        current_user.points += challenge.points_reward
        update_streak(current_user)
        update_user_level(current_user)
        check_and_award_badges(current_user, 'challenge_complete' if user_challenge.progress == 100 else 'general')
        check_and_award_certificates(current_user, context='challenge_complete')

    db.session.commit()
    return jsonify({'message': 'Progress updated', 'new_progress': user_challenge.progress})

@app.route('/api/user/<int:user_id>/rewards', methods=['GET'])
@token_required
def get_rewards(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    # Badges
    user_badges = db.session.query(UserBadge, Badge).join(Badge).filter(UserBadge.user_id == user_id).all()
    badges = []
    for ub, badge in user_badges:
        badges.append({
            'id': badge.id,
            'name': badge.name,
            'description': badge.description,
            'icon': badge.icon,
            'earned_at': ub.earned_at.isoformat()
        })

    # Certificates
    user_certs = db.session.query(UserCertificate, Certificate).join(Certificate).filter(UserCertificate.user_id == user_id).all()
    certificates = []
    for uc, cert in user_certs:
        certificates.append({
            'id': cert.id,
            'name': cert.name,
            'description': cert.description,
            'icon': cert.icon,
            'earned_at': uc.earned_at.isoformat(),
            'score': uc.score
        })

    # Streak milestones (computed)
    streak_milestones = [
        {'days': 7, 'unlocked': current_user.streak_days >= 7, 'points': 100},
        {'days': 14, 'unlocked': current_user.streak_days >= 14, 'points': 250},
        {'days': 30, 'unlocked': current_user.streak_days >= 30, 'points': 500},
        {'days': 100, 'unlocked': current_user.streak_days >= 100, 'points': 1000}
    ]

    return jsonify({
        'badges': badges,
        'certificates': certificates,
        'streak_milestones': streak_milestones,
        'unlockables': [
            {'name': 'Advanced Games', 'unlocked': current_user.level >= 10},
            {'name': 'Premium Challenges', 'unlocked': current_user.streak_days >= 50}
        ]
    })

@app.route('/api/user/<int:user_id>/certificates/<int:cert_id>/download', methods=['GET'])
@token_required
def download_certificate(current_user, user_id, cert_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    user_cert = UserCertificate.query.filter_by(user_id=user_id, certificate_id=cert_id).first()
    if not user_cert:
        return jsonify({'message': 'Certificate not found'}), 404

    cert = Certificate.query.get(cert_id)
    # In production, generate PDF with user details, date, score, etc.
    # For now, return JSON data for frontend to handle download (e.g., generate PDF client-side)
    return jsonify({
        'certificate': {
            'name': cert.name,
            'description': cert.description,
            'earned_at': user_cert.earned_at.isoformat(),
            'score': user_cert.score,
            'user': current_user.username,
            'level': current_user.level
        },
        'message': 'Certificate data ready for download'
    })

@app.route('/api/leaderboard', methods=['GET'])
@token_required
def get_leaderboard(current_user):
    # Top users by points (limit to 10 for performance)
    top_users = User.query.order_by(User.points.desc()).limit(10).all()
    leaderboard = []
    for i, user in enumerate(top_users, 1):
        rank = f"#{i}"
        if i == 1:
            rank = "🥇"
        elif i == 2:
            rank = "🥈"
        elif i == 3:
            rank = "🥉"
        leaderboard.append({
            'rank': rank,
            'username': user.username,
            'points': user.points,
            'level': user.level,
            'streak_days': user.streak_days
        })

    # User's rank
    all_users = User.query.order_by(User.points.desc())