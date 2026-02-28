from flask import Blueprint, request, jsonify
from app.models import Post, PostStatus, PostLike
from app.services.post_service import create_post, approve_post, reject_post, get_posts
from .auth import login_required, admin_required
from app import db
from app.log import log

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

@posts_bp.route('', methods=['POST'])
@login_required
def create_post_api():
    data = request.json
    title = data.get('title')
    content_html = data.get('content_html')
    category_id = data.get('category_id')
    
    if not title or not content_html or not category_id:
        return jsonify({'error': '缺少必要参数'}), 400
    
    from flask import session
    author_id = session['user_id']
    
    post = create_post(title, content_html, category_id, author_id)

    log(f'用户{session["user_id"]}创建了帖子：{title}')

    return jsonify({
        'id': post.id,
        'title': post.title,
        'content_html': post.content_html,
        'content_excerpt': post.content_excerpt,
        'author_id': post.author_id,
        'category_id': post.category_id,
        'status': post.status,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat()
    })

@posts_bp.route('', methods=['GET'])
def get_posts_api():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    category = request.args.get('category', type=int)
    status = request.args.get('status')
    sort = request.args.get('sort')
    
    result = get_posts(page, page_size, category, status, sort)
    
    posts_data = []
    for post in result['items']:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'content_excerpt': post.content_excerpt,
            'author_id': post.author_id,
            'author_username': post.author.username,
            'category_id': post.category_id,
            'category_name': post.category.name,
            'status': post.status,
            'views': post.views,
            'comments_count': post.comments.count(),
            'likes_count': post.likes.count(),
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat()
        })
    
    return jsonify({
        'items': posts_data,
        'total': result['total'],
        'page': result['page'],
        'page_size': result['page_size']
    })

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post_detail(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    # 检查权限：如果帖子未通过审核，只有作者或管理员可以查看
    from flask import session
    user_id = session.get('user_id')
    if post.status != PostStatus.APPROVED and not (user_id and (user_id == post.author_id or post.author.is_admin)):
        return jsonify({'error': '无权查看此帖子'}), 403
    
    # 增加浏览次数
    post.views += 1
    from app import db
    db.session.commit()
    
    # 获取点赞信息
    from flask import session
    user_id = session.get('user_id')
    is_liked = False
    likes_count = post.likes.count()
    
    if user_id:
        existing_like = PostLike.query.filter_by(user_id=user_id, post_id=post.id).first()
        is_liked = existing_like is not None
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content_html': post.content_html,
        'author_id': post.author_id,
        'author_username': post.author.username,
        'category_id': post.category_id,
        'category_name': post.category.name,
        'status': post.status,
        'views': post.views,
        'comments_count': post.comments.count(),
        'likes_count': likes_count,
        'is_liked': is_liked,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat()
    })

@posts_bp.route('/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    from flask import session
    user_id = session['user_id']
    
    # 检查是否已经点赞
    existing_like = PostLike.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing_like:
        return jsonify({'error': '已经点赞过了'}), 400
    
    # 创建点赞记录
    new_like = PostLike(user_id=user_id, post_id=post_id)
    db.session.add(new_like)
    db.session.commit()

    log(f'用户{session["user_id"]}点赞了帖子：{post.title}')

    return jsonify({'message': '点赞成功'})

@posts_bp.route('/<int:post_id>/like', methods=['DELETE'])
@login_required
def unlike_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    from flask import session
    user_id = session['user_id']
    
    # 查找点赞记录
    existing_like = PostLike.query.filter_by(user_id=user_id, post_id=post_id).first()
    if not existing_like:
        return jsonify({'error': '还没有点赞'}), 400
    
    # 删除点赞记录
    db.session.delete(existing_like)
    db.session.commit()

    log(f'用户{session["user_id"]}取消点赞了帖子：{post.title}')

    return jsonify({'message': '取消点赞成功'})

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    # 先删除相关的点赞记录
    from app.models import PostLike, Comment, CommentLike
    PostLike.query.filter_by(post_id=post_id).delete()
    
    # 删除相关的评论及其点赞记录
    comments = Comment.query.filter_by(post_id=post_id).all()
    for comment in comments:
        CommentLike.query.filter_by(comment_id=comment.id).delete()
    Comment.query.filter_by(post_id=post_id).delete()
    
    # 删除帖子
    db.session.delete(post)
    db.session.commit()

    log(f'管理员删除了帖子：{post.title}')

    return jsonify({'message': '帖子删除成功'})

@posts_bp.route('/<int:post_id>', methods=['PUT'])
@admin_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    data = request.json
    title = data.get('title')
    content_html = data.get('content_html')
    category_id = data.get('category_id')
    status = data.get('status')
    
    if title:
        post.title = title
    if content_html:
        post.content_html = content_html
        # 更新摘要
        import re
        plain_text = re.sub(r'<[^<]+?>', '', content_html)
        post.content_excerpt = plain_text[:200] + '...' if len(plain_text) > 200 else plain_text
    if category_id:
        post.category_id = category_id
    if status:
        post.status = status
    
    db.session.commit()

    log(f'管理员更新了帖子：{post.title}')

    return jsonify({
        'id': post.id,
        'title': post.title,
        'content_html': post.content_html,
        'content_excerpt': post.content_excerpt,
        'author_id': post.author_id,
        'category_id': post.category_id,
        'status': post.status,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat()
    })
