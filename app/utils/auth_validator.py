from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.models.user import User

def admin_required():
    """
    Decorator to check if the current user has admin privileges.
    Must be used after jwt_required() decorator.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("is_admin"):
                return fn(*args, **kwargs)
            return jsonify({"msg": "Admin privileges required"}), 403
        return decorator
    return wrapper

def teacher_required():
    """
    Decorator to check if the current user is a teacher.
    Must be used after jwt_required() decorator.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("is_teacher"):
                return fn(*args, **kwargs)
            return jsonify({"msg": "Teacher privileges required"}), 403
        return decorator
    return wrapper

def validate_user_exists(user_id):
    """
    Helper function to validate if a user exists.
    Returns the user object if found, otherwise returns None.
    """
    return User.query.get(user_id)