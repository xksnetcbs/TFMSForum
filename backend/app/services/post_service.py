from app.models import Post, PostStatus
from app import db
from .notification_service import send_notification, send_notification_to_admins


def create_post(title, content_markdown, category_id, author_id):
    """创建新帖子"""
    # 生成摘要
    content_excerpt = content_markdown[:300] + ('...' if len(content_markdown) > 300 else '')
    
    post = Post(
        title=title,
        content_markdown=content_markdown,
        content_excerpt=content_excerpt,
        category_id=category_id,
        author_id=author_id,
        status=PostStatus.PENDING
    )
    
    db.session.add(post)
    db.session.commit()
    
    # 给所有管理员发送通知
    send_notification_to_admins(
        "新帖子待审核",
        f"用户 {post.author.username} 发布了新帖子《{post.title}》，等待审核。"
    )
    
    return post


def approve_post(post_id):
    """审核通过帖子"""
    post = Post.query.get(post_id)
    if not post:
        return None
    
    post.status = PostStatus.APPROVED
    db.session.commit()
    
    # 给作者发送通知
    send_notification(
        post.author_id,
        "帖子审核通过",
        f"你的帖子《{post.title}》已通过审核。"
    )
    
    return post


def reject_post(post_id, reason=""):
    """拒绝帖子"""
    post = Post.query.get(post_id)
    if not post:
        return None
    
    post.status = PostStatus.REJECTED
    db.session.commit()
    
    # 给作者发送通知
    content = f"你的帖子《{post.title}》未通过审核。"
    if reason:
        content += f" 原因：{reason}"
    
    send_notification(
        post.author_id,
        "帖子审核未通过",
        content
    )
    
    return post


def get_posts(page=1, page_size=10, category=None, status=None, sort=None):
    """获取帖子列表"""
    query = Post.query
    
    if category:
        query = query.filter_by(category_id=category)
    
    if status:
        query = query.filter_by(status=status)
    
    if sort == 'latest':
        query = query.order_by(Post.created_at.desc())
    elif sort == 'hot':
        # 简单的热门排序，按评论数
        query = query.outerjoin(Post.comments).group_by(Post.id).order_by(db.func.count(Post.comments).desc())
    else:
        query = query.order_by(Post.created_at.desc())
    
    total = query.count()
    posts = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        'items': posts,
        'total': total,
        'page': page,
        'page_size': page_size
    }
