from datetime import datetime, timedelta
from app.models.analytics import UserAnalytics, SchoolAnalytics
from app.models.eco_impact import UserEcoAction
from app.models.learning import ModuleCompletion
from app.models.user import User
from app import db

def update_user_analytics(user_id):
    """
    Updates analytics for a specific user.
    """
    user = User.query.get(user_id)
    if not user:
        return False
    
    # Get time ranges
    now = datetime.utcnow()
    last_week = now - timedelta(days=7)
    last_month = now - timedelta(days=30)
    
    # Calculate metrics
    eco_actions_week = UserEcoAction.query.filter(
        UserEcoAction.user_id == user_id,
        UserEcoAction.created_at >= last_week
    ).count()
    
    eco_actions_month = UserEcoAction.query.filter(
        UserEcoAction.user_id == user_id,
        UserEcoAction.created_at >= last_month
    ).count()
    
    modules_completed_week = ModuleCompletion.query.filter(
        ModuleCompletion.user_id == user_id,
        ModuleCompletion.completed_at >= last_week
    ).count()
    
    modules_completed_month = ModuleCompletion.query.filter(
        ModuleCompletion.user_id == user_id,
        ModuleCompletion.completed_at >= last_month
    ).count()
    
    # Update or create analytics record
    analytics = UserAnalytics.query.filter_by(user_id=user_id).first()
    if not analytics:
        analytics = UserAnalytics(user_id=user_id)
        db.session.add(analytics)
    
    analytics.eco_actions_week = eco_actions_week
    analytics.eco_actions_month = eco_actions_month
    analytics.modules_completed_week = modules_completed_week
    analytics.modules_completed_month = modules_completed_month
    analytics.last_updated = now
    
    db.session.commit()
    return True

def update_school_analytics(school_id):
    """
    Updates analytics for a specific school.
    """
    # Get all users in the school
    users = User.query.filter_by(school_id=school_id).all()
    if not users:
        return False
    
    now = datetime.utcnow()
    last_month = now - timedelta(days=30)
    
    total_eco_actions = 0
    total_modules_completed = 0
    active_users = 0
    
    for user in users:
        # Count eco actions
        eco_actions = UserEcoAction.query.filter(
            UserEcoAction.user_id == user.id,
            UserEcoAction.created_at >= last_month
        ).count()
        total_eco_actions += eco_actions
        
        # Count completed modules
        modules = ModuleCompletion.query.filter(
            ModuleCompletion.user_id == user.id,
            ModuleCompletion.completed_at >= last_month
        ).count()
        total_modules_completed += modules
        
        # Check if user is active
        if eco_actions > 0 or modules > 0:
            active_users += 1
    
    # Update or create school analytics record
    analytics = SchoolAnalytics.query.filter_by(school_id=school_id).first()
    if not analytics:
        analytics = SchoolAnalytics(school_id=school_id)
        db.session.add(analytics)
    
    analytics.total_eco_actions = total_eco_actions
    analytics.total_modules_completed = total_modules_completed
    analytics.active_users = active_users
    analytics.total_users = len(users)
    analytics.last_updated = now
    
    db.session.commit()
    return True

def get_user_statistics(user_id):
    """
    Returns comprehensive statistics for a user.
    """
    analytics = UserAnalytics.query.filter_by(user_id=user_id).first()
    if not analytics:
        return None
    
    return {
        "eco_actions": {
            "week": analytics.eco_actions_week,
            "month": analytics.eco_actions_month
        },
        "learning": {
            "modules_completed_week": analytics.modules_completed_week,
            "modules_completed_month": analytics.modules_completed_month
        },
        "last_updated": analytics.last_updated
    }

def get_school_statistics(school_id):
    """
    Returns comprehensive statistics for a school.
    """
    analytics = SchoolAnalytics.query.filter_by(school_id=school_id).first()
    if not analytics:
        return None
    
    return {
        "total_eco_actions": analytics.total_eco_actions,
        "total_modules_completed": analytics.total_modules_completed,
        "user_engagement": {
            "active_users": analytics.active_users,
            "total_users": analytics.total_users,
            "engagement_rate": (analytics.active_users / analytics.total_users * 100) if analytics.total_users > 0 else 0
        },
        "last_updated": analytics.last_updated
    }