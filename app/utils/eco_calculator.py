from datetime import datetime
from app.models.eco_impact import EcoAction, UserEcoAction, CommunityProject
from app.models.user import User
from app.utils.achievement_handler import check_eco_achievements
from app import db

def log_eco_action(user_id, action_id, quantity=1):
    """
    Records an eco-friendly action performed by a user.
    Returns the impact value generated.
    """
    action = EcoAction.query.get(action_id)
    if not action:
        return None
    
    impact_value = action.impact_per_unit * quantity
    
    user_action = UserEcoAction(
        user_id=user_id,
        action_id=action_id,
        quantity=quantity,
        impact_value=impact_value
    )
    
    db.session.add(user_action)
    db.session.commit()
    
    # Check for potential achievements
    check_eco_achievements(user_id)
    
    return impact_value

def get_user_impact(user_id):
    """
    Calculates the total environmental impact for a user.
    """
    user_actions = UserEcoAction.query.filter_by(user_id=user_id).all()
    
    total_impact = sum(action.impact_value for action in user_actions)
    action_breakdown = {}
    
    for action in user_actions:
        eco_action = EcoAction.query.get(action.action_id)
        if eco_action.name not in action_breakdown:
            action_breakdown[eco_action.name] = {
                "count": 0,
                "total_impact": 0
            }
        action_breakdown[eco_action.name]["count"] += action.quantity
        action_breakdown[eco_action.name]["total_impact"] += action.impact_value
    
    return {
        "total_impact": total_impact,
        "actions_taken": len(user_actions),
        "breakdown": action_breakdown
    }

def create_community_project(name, description, goal, creator_id):
    """
    Creates a new community environmental project.
    """
    project = CommunityProject(
        name=name,
        description=description,
        goal=goal,
        creator_id=creator_id,
        status="active"
    )
    
    db.session.add(project)
    db.session.commit()
    return project

def update_project_progress(project_id, new_progress):
    """
    Updates the progress of a community project.
    Returns True if the project is completed, False otherwise.
    """
    project = CommunityProject.query.get(project_id)
    if not project:
        return False
    
    project.current_progress = new_progress
    project.last_updated = datetime.utcnow()
    
    if project.current_progress >= project.goal:
        project.status = "completed"
        project.completion_date = datetime.utcnow()
        completed = True
    else:
        completed = False
    
    db.session.commit()
    return completed

def get_school_impact(school_id):
    """
    Calculates the total environmental impact for a school.
    """
    # Get all users in the school
    users = User.query.filter_by(school_id=school_id).all()
    if not users:
        return None
    
    total_impact = 0
    total_actions = 0
    action_breakdown = {}
    
    for user in users:
        user_actions = UserEcoAction.query.filter_by(user_id=user.id).all()
        total_actions += len(user_actions)
        
        for action in user_actions:
            total_impact += action.impact_value
            eco_action = EcoAction.query.get(action.action_id)
            
            if eco_action.name not in action_breakdown:
                action_breakdown[eco_action.name] = {
                    "count": 0,
                    "total_impact": 0
                }
            action_breakdown[eco_action.name]["count"] += action.quantity
            action_breakdown[eco_action.name]["total_impact"] += action.impact_value
    
    return {
        "total_impact": total_impact,
        "total_actions": total_actions,
        "participating_users": len(users),
        "breakdown": action_breakdown
    }