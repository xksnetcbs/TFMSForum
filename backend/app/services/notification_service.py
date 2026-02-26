from app.models import Notification, User
from app import db


def send_notification(user_id, title, content):
    """发送站内信通知"""
    notification = Notification(
        user_id=user_id,
        title=title,
        content=content
    )
    db.session.add(notification)
    db.session.commit()


def send_notification_to_admins(title, content):
    """给所有管理员发送通知"""
    admins = User.query.filter_by(is_admin=True).all()
    for admin in admins:
        send_notification(admin.id, title, content)


def mark_notification_as_read(notification_id, user_id):
    """标记通知为已读"""
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if notification:
        notification.is_read = True
        db.session.commit()
        return True
    return False


def mark_all_notifications_as_read(user_id):
    """标记所有通知为已读"""
    notifications = Notification.query.filter_by(user_id=user_id).all()
    for notification in notifications:
        notification.is_read = True
    db.session.commit()
