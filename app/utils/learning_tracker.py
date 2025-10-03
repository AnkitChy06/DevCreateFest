from datetime import datetime
from app.models.learning import LearningPath, LearningModule, ModuleCompletion
from app.models.user import User
from app import db

def get_user_progress(user_id, path_id=None):
    """
    Gets the learning progress for a user.
    If path_id is provided, returns progress for that specific path.
    Otherwise, returns progress for all paths.
    """
    user = User.query.get(user_id)
    if not user:
        return None
    
    if path_id:
        # Get progress for specific path
        path = LearningPath.query.get(path_id)
        if not path:
            return None
        
        modules = LearningModule.query.filter_by(path_id=path_id).all()
        completed_modules = ModuleCompletion.query.filter_by(
            user_id=user_id
        ).filter(
            ModuleCompletion.module_id.in_([m.id for m in modules])
        ).all()
        
        completed_ids = [cm.module_id for cm in completed_modules]
        total_modules = len(modules)
        completed_count = len(completed_modules)
        
        return {
            "path_id": path_id,
            "path_name": path.name,
            "progress": (completed_count / total_modules * 100) if total_modules > 0 else 0,
            "completed_modules": completed_count,
            "total_modules": total_modules,
            "modules": [{
                "id": module.id,
                "name": module.name,
                "completed": module.id in completed_ids,
                "completion_date": next(
                    (cm.completed_at for cm in completed_modules if cm.module_id == module.id),
                    None
                )
            } for module in modules]
        }
    else:
        # Get progress for all paths
        paths = LearningPath.query.all()
        progress = []
        
        for path in paths:
            modules = LearningModule.query.filter_by(path_id=path.id).all()
            completed_modules = ModuleCompletion.query.filter_by(
                user_id=user_id
            ).filter(
                ModuleCompletion.module_id.in_([m.id for m in modules])
            ).all()
            
            total_modules = len(modules)
            completed_count = len(completed_modules)
            
            progress.append({
                "path_id": path.id,
                "path_name": path.name,
                "progress": (completed_count / total_modules * 100) if total_modules > 0 else 0,
                "completed_modules": completed_count,
                "total_modules": total_modules
            })
        
        return progress

def mark_module_complete(user_id, module_id):
    """
    Marks a learning module as completed for a user.
    Returns True if newly completed, False if already completed.
    """
    # Check if already completed
    existing = ModuleCompletion.query.filter_by(
        user_id=user_id,
        module_id=module_id
    ).first()
    
    if existing:
        return False
    
    completion = ModuleCompletion(
        user_id=user_id,
        module_id=module_id,
        completed_at=datetime.utcnow()
    )
    
    db.session.add(completion)
    db.session.commit()
    return True

def get_recommended_modules(user_id):
    """
    Returns recommended learning modules based on user's progress.
    """
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Get completed modules
    completed_modules = ModuleCompletion.query.filter_by(user_id=user_id).all()
    completed_ids = [cm.module_id for cm in completed_modules]
    
    recommendations = []
    paths = LearningPath.query.all()
    
    for path in paths:
        modules = LearningModule.query.filter_by(path_id=path.id).order_by(LearningModule.order).all()
        
        # Find first uncompleted module in path
        for module in modules:
            if module.id not in completed_ids:
                recommendations.append({
                    "path_id": path.id,
                    "path_name": path.name,
                    "module_id": module.id,
                    "module_name": module.name,
                    "description": module.description,
                    "prerequisites_completed": all(
                        prereq.id in completed_ids 
                        for prereq in modules 
                        if prereq.order < module.order
                    )
                })
                break
    
    return recommendations

def reset_module_progress(user_id, module_id):
    """
    Resets the completion status of a module for a user.
    Returns True if progress was reset, False if no completion record existed.
    """
    completion = ModuleCompletion.query.filter_by(
        user_id=user_id,
        module_id=module_id
    ).first()
    
    if not completion:
        return False
    
    db.session.delete(completion)
    db.session.commit()
    return True