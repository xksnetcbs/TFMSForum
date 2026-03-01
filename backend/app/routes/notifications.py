from flask import Blueprint, request, jsonify
from app.models import Notification
from app.services.notification_service import mark_notification_as_read, mark_all_notifications_as_read
from .auth import login_required
from app.log import log

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notifications_bp.route('', methods=['GET'])
@login_required
def get_notifications():
    from flask import session
    user_id = session['user_id']
    
    unread_only = request.args.get('unread', type=int)
    query = Notification.query.filter_by(user_id=user_id)
    
    if unread_only:
        query = query.filter_by(is_read=False)
    
    notifications = query.order_by(Notification.created_at.desc()).all()
    
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'content': notification.content,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat()
        })
    
    return jsonify(notifications_data)

@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_as_read(notification_id):
    from flask import session
    user_id = session['user_id']
    
    success = mark_notification_as_read(notification_id, user_id)
    if not success:
        return jsonify({'error': '通知不存在或无权操作'}), 404

    log(f'用户id: {user_id}标记了通知id: {notification_id}为已读')
    return jsonify({'message': '标记已读成功'})

@notifications_bp.route('/read_all', methods=['POST'])
@login_required
def mark_all_as_read():
    from flask import session
    user_id = session['user_id']
    
    mark_all_notifications_as_read(user_id)
    log(f'用户id: {user_id}标记了所有通知为已读')
    return jsonify({'message': '全部标记已读成功'})

@notifications_bp.route('/send', methods=['POST'])
@login_required
def send_notification():
    from flask import session, request
    user_id = session['user_id']
    
    # 检查是否为管理员
    from app.models import User
    current_user = User.query.get(user_id)
    if not current_user.is_admin:
        return jsonify({'error': '只有管理员可以发送站内信'}), 403
    
    data = request.get_json()
    user_ids = data.get('user_ids', [])
    title = data.get('title', '')
    content = data.get('content', '')
    
    if not user_ids or not title or not content:
        return jsonify({'error': '用户ID、标题和内容不能为空'}), 400
    
    from app.services.notification_service import send_notification as send_notif
    for target_user_id in user_ids:
        send_notif(target_user_id, title, content)
    
    log(f'管理员id: {user_id}向用户id: {user_ids}发送了站内信')
    return jsonify({'message': '站内信发送成功'})
