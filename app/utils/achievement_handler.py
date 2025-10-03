from app.models.achievement import Achievement, UserAchievement
from app.models.gamification import UserPoints
from app.models.eco_impact import EcoAction, UserEcoAction
from app.models.user import User
from app.models.social import Notification
from app import db

def award_achievement(user_id, achievement_id):
    """
    Awards an achievement to a user if they don't already have it.
    Returns True if awarded, False if already owned.
    """
    if UserAchievement.query.filter_by(user_id=user_id, achievement_id=achievement_id).first():
        return False
    
    achievement = Achievement.query.get(achievement_id)
    if not achievement:
        return False
    
    new_user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement_id)
    db.session.add(new_user_achievement)
    
    # Award points for achievement
    user_points = UserPoints.query.filter_by(user_id=user_id).first()
    if not user_points:
        user_points = UserPoints(user_id=user_id, points=achievement.points)
        db.session.add(user_points)
    else:
        user_points.points += achievement.points
    
    # Create notification for achievement
    notification = Notification(
        user_id=user_id,
        type="achievement",
        content=f"Congratulations! You've earned the {achievement.name} achievement!",
        data={"achievement_id": achievement_id, "points": achievement.points}
    )
    db.session.add(notification)
    
    db.session.commit()
    return True

def check_eco_achievements(user_id):
    """
    Checks and awards eco-related achievements based on user's actions.
    """
    user_actions = UserEcoAction.query.filter_by(user_id=user_id).all()
    total_actions = len(user_actions)
    total_impact = sum(action.impact_value for action in user_actions)
    
    # Example achievement criteria
    achievements = {
        "eco_starter": {"count": 1, "achievement_id": 1},  # First eco action
        "eco_enthusiast": {"count": 5, "achievement_id": 2},  # 5 eco actions
        "eco_warrior": {"count": 10, "achievement_id": 3},  # 10 eco actions
        "climate_hero": {"impact": 100, "achievement_id": 4}  # 100 total impact
    }
    
    # Check and award achievements
    if total_actions >= 1:
        award_achievement(user_id, achievements["eco_starter"]["achievement_id"])
    if total_actions >= 5:
        award_achievement(user_id, achievements["eco_enthusiast"]["achievement_id"])
    if total_actions >= 10:
        award_achievement(user_id, achievements["eco_warrior"]["achievement_id"])
    if total_impact >= 100:
        award_achievement(user_id, achievements["climate_hero"]["achievement_id"])

def get_user_achievements(user_id):
    """
    Returns all achievements earned by a user.
    """
    user_achievements = UserAchievement.query.filter_by(user_id=user_id).all()
    achievements = []
    for ua in user_achievements:
        achievement = Achievement.query.get(ua.achievement_id)
        if achievement:
            achievements.append({
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "points": achievement.points,
                "earned_at": ua.earned_at
            })
    return achievements