from flask import Blueprint, request, jsonify
from app.models import Comment, CommentLike, User
from app import db
from .auth import login_required

comments_bp = Blueprint('comments', __name__, url_prefix='/api')

@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
    
    comments_data = []
    from flask import session
    user_id = session.get('user_id')
    
    for comment in comments:
        # 获取评论的点赞信息
        likes_count = comment.likes.count()
        is_liked = False
        
        if user_id:
            existing_like = CommentLike.query.filter_by(user_id=user_id, comment_id=comment.id).first()
            is_liked = existing_like is not None
        
        comments_data.append({
            'id': comment.id,
            'post_id': comment.post_id,
            'author_id': comment.author_id,
            'author_username': comment.author.username,
            'content': comment.content,
            'likes_count': likes_count,
            'is_liked': is_liked,
            'created_at': comment.created_at.isoformat(),
            'updated_at': comment.updated_at.isoformat()
        })
    
    return jsonify(comments_data)

@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def create_comment(post_id):
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'error': '缺少评论内容'}), 400
    
    from flask import session
    author_id = session['user_id']
    
    comment = Comment(
        post_id=post_id,
        author_id=author_id,
        content=content
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'id': comment.id,
        'post_id': comment.post_id,
        'author_id': comment.author_id,
        'author_username': comment.author.username,
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat()
    })

@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': '评论不存在'}), 404
    
    from flask import session
    user_id = session['user_id']
    
    # 只有评论作者或管理员可以删除评论
    from app.models import User
    user = User.query.get(user_id)
    if not (user_id == comment.author_id or user.is_admin):
        return jsonify({'error': '无权删除此评论'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': '评论删除成功'})

@comments_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
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
        return jsonify({'error': '已经点赞过了'}), 400
    
    # 创建点赞记录
    new_like = CommentLike(user_id=user_id, comment_id=comment_id)
    db.session.add(new_like)
    db.session.commit()
    
    return jsonify({'message': '点赞成功'})

@comments_bp.route('/comments/<int:comment_id>/like', methods=['DELETE'])
@login_required
def unlike_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': '评论不存在'}), 404
    
    from flask import session
    user_id = session['user_id']
    
    # 查找点赞记录
    existing_like = CommentLike.query.filter_by(user_id=user_id, comment_id=comment_id).first()
    if not existing_like:
        return jsonify({'error': '还没有点赞'}), 400
    
    # 删除点赞记录
    db.session.delete(existing_like)
    db.session.commit()
    
    return jsonify({'message': '取消点赞成功'})
