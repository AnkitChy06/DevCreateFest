from datetime import datetime, timedelta
import logging
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from app import db

def db_operation(f):
    """
    Decorator for database operations that handles errors and rollbacks.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Database error in {f.__name__}: {str(e)}")
            raise
        except Exception as e:
            db.session.rollback()
            logging.error(f"Unexpected error in {f.__name__}: {str(e)}")
            raise
    return decorated_function

def parse_date(date_str):
    """
    Safely parse a date string into a datetime object.
    Returns None if parsing fails.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def date_range(start_date, end_date):
    """
    Generate a list of dates between start_date and end_date (inclusive).
    """
    if not isinstance(start_date, datetime):
        start_date = parse_date(start_date)
    if not isinstance(end_date, datetime):
        end_date = parse_date(end_date)
    
    if not start_date or not end_date:
        return []
    
    date_list = []
    current_date = start_date
    
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    
    return date_list

def paginate_query(query, page=1, per_page=10):
    """
    Helper function to paginate SQLAlchemy queries.
    Returns tuple of (items, total_pages, total_items).
    """
    if page < 1:
        page = 1
    
    total = query.count()
    total_pages = (total + per_page - 1) // per_page
    
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return items, total_pages, total

def validate_data(data, required_fields):
    """
    Validates that all required fields are present in the data.
    Returns tuple of (is_valid, missing_fields).
    """
    if not data:
        return False, required_fields
    
    missing = [field for field in required_fields if field not in data]
    return len(missing) == 0, missing

def format_timedelta(delta):
    """
    Formats a timedelta into a human-readable string.
    """
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    
    parts = []
    if days:
        parts.append(f"{days} {'day' if days == 1 else 'days'}")
    if hours:
        parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
    if minutes:
        parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
    
    if not parts:
        return "just now"
    
    return ", ".join(parts) + " ago"

def time_ago(date):
    """
    Converts a datetime to a "time ago" string.
    """
    if not date:
        return None
    
    now = datetime.utcnow()
    delta = now - date
    
    return format_timedelta(delta)

def safe_commit():
    """
    Safely commits changes to the database with error handling.
    Returns True if successful, False if error occurred.
    """
    try:
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database commit error: {str(e)}")
        return False
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error during commit: {str(e)}")
        return False