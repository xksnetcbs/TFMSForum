from flask import Blueprint, request, jsonify
from app.models import PostLike, CommentLike, Post, Comment
from app import db
from app.log import log
from .auth import login_required

likes_bp = Blueprint('likes', __name__, url_prefix='/api')

@likes_bp.route('/posts/<int:post_id>/like', methods=['POST'])
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
        return jsonify({'error': '已经点赞过'}), 400
    
    # 创建点赞记录
    like = PostLike(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    
    # 返回点赞数
    likes_count = PostLike.query.filter_by(post_id=post_id).count()

    log(f'用户id: {user_id} 点赞了帖子 {post_id}: {post.title}')

    return jsonify({
        'message': '点赞成功',
        'likes_count': likes_count
    })

@likes_bp.route('/posts/<int:post_id>/unlike', methods=['POST'])
@login_required
def unlike_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    from flask import session
    user_id = session['user_id']
    
    # 查找并删除点赞记录
    like = PostLike.query.filter_by(user_id=user_id, post_id=post_id).first()
    if not like:
        return jsonify({'error': '未点赞过'}), 400
    
    db.session.delete(like)
    db.session.commit()
    
    # 返回点赞数
    likes_count = PostLike.query.filter_by(post_id=post_id).count()

    log(f'用户id: {user_id} 取消点赞了帖子 {post_id}: {post.title}')

    return jsonify({
        'message': '取消点赞成功',
        'likes_count': likes_count
    })

@likes_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': '评论不存在'}), 404
    
    from flask import session
    user_id = session['user_id']
    
    # 检查是否已经点赞
    existing_like = CommentLike.query.filter_by(user_id=user_id, comment_id=comment_id).first()
    if existing_like:
        return jsonify({'error': '已经点赞过'}), 400
    
    # 创建点赞记录
    like = CommentLike(user_id=user_id, comment_id=comment_id)
    db.session.add(like)
    db.session.commit()
    
    # 返回点赞数
    likes_count = CommentLike.query.filter_by(comment_id=comment_id).count()
    
    return jsonify({
        'message': '点赞成功',
        'likes_count': likes_count
    })

@likes_bp.route('/comments/<int:comment_id>/unlike', methods=['POST'])
@login_required
def unlike_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': '评论不存在'}), 404
    
    from flask import session
    user_id = session['user_id']
    
    # 查找并删除点赞记录
    like = CommentLike.query.filter_by(user_id=user_id, comment_id=comment_id).first()
    if not like:
        return jsonify({'error': '未点赞过'}), 400
    
    db.session.delete(like)
    db.session.commit()
    
    # 返回点赞数
    likes_count = CommentLike.query.filter_by(comment_id=comment_id).count()
    
    return jsonify({
        'message': '取消点赞成功',
        'likes_count': likes_count
    })
