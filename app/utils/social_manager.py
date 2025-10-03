from datetime import datetime
from app.models.social import UserConnection, Notification
from app.models.user import User
from app import db

def create_connection(user_id, friend_id):
    """
    Creates a connection between two users.
    Returns True if connection was created, False if it already exists.
    """
    if user_id == friend_id:
        return False
    
    existing = UserConnection.query.filter(
        ((UserConnection.user_id == user_id) & (UserConnection.friend_id == friend_id)) |
        ((UserConnection.user_id == friend_id) & (UserConnection.friend_id == user_id))
    ).first()
    
    if existing:
        return False
    
    connection = UserConnection(
        user_id=user_id,
        friend_id=friend_id,
        status="pending"
    )
    
    # Create notification for friend request
    notification = Notification(
        user_id=friend_id,
        type="friend_request",
        content=f"You have a new friend request!",
        data={"from_user_id": user_id}
    )
    
    db.session.add(connection)
    db.session.add(notification)
    db.session.commit()
    return True

def accept_connection(user_id, friend_id):
    """
    Accepts a pending connection request.
    Returns True if successful, False if connection doesn't exist or is already accepted.
    """
    connection = UserConnection.query.filter_by(
        user_id=friend_id,
        friend_id=user_id,
        status="pending"
    ).first()
    
    if not connection:
        return False
    
    connection.status = "accepted"
    connection.accepted_at = datetime.utcnow()
    
    # Create notification for accepted request
    notification = Notification(
        user_id=friend_id,
        type="friend_accepted",
        content=f"Your friend request was accepted!",
        data={"friend_id": user_id}
    )
    
    db.session.add(notification)
    db.session.commit()
    return True

def get_user_connections(user_id, status=None):
    """
    Gets all connections for a user.
    Optional status filter: 'pending', 'accepted'
    """
    query = UserConnection.query.filter(
        (UserConnection.user_id == user_id) |
        (UserConnection.friend_id == user_id)
    )
    
    if status:
        query = query.filter_by(status=status)
    
    connections = query.all()
    result = []
    
    for conn in connections:
        friend_id = conn.friend_id if conn.user_id == user_id else conn.user_id
        friend = User.query.get(friend_id)
        
        if friend:
            result.append({
                "user_id": friend.id,
                "username": friend.username,
                "status": conn.status,
                "connected_since": conn.accepted_at if conn.status == "accepted" else None
            })
    
    return result

def remove_connection(user_id, friend_id):
    """
    Removes a connection between users.
    Returns True if connection was removed, False if it didn't exist.
    """
    connection = UserConnection.query.filter(
        ((UserConnection.user_id == user_id) & (UserConnection.friend_id == friend_id)) |
        ((UserConnection.user_id == friend_id) & (UserConnection.friend_id == user_id))
    ).first()
    
    if not connection:
        return False
    
    db.session.delete(connection)
    db.session.commit()
    return True

def create_notification(user_id, notification_type, content, data=None):
    """
    Creates a new notification for a user.
    """
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        content=content,
        data=data
    )
    
    db.session.add(notification)
    db.session.commit()
    return notification

def get_user_notifications(user_id, unread_only=False):
    """
    Gets notifications for a user.
    Optional filter for unread notifications only.
    """
    query = Notification.query.filter_by(user_id=user_id)
    
    if unread_only:
        query = query.filter_by(read=False)
    
    notifications = query.order_by(Notification.created_at.desc()).all()
    
    return [{
        "id": notif.id,
        "type": notif.type,
        "content": notif.content,
        "data": notif.data,
        "created_at": notif.created_at,
        "read": notif.read
    } for notif in notifications]

def mark_notification_read(notification_id, user_id):
    """
    Marks a notification as read.
    Returns True if successful, False if notification doesn't exist or belong to user.
    """
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user_id
    ).first()
    
    if not notification:
        return False
    
    notification.read = True
    notification.read_at = datetime.utcnow()
    db.session.commit()
    return True