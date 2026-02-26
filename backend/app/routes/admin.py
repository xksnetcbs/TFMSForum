from flask import Blueprint, request, jsonify
from app.models import Post
from app.services.post_service import approve_post, reject_post
from .auth import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/posts/pending', methods=['GET'])
@admin_required
def get_pending_posts():
    posts = Post.query.filter_by(status='pending').order_by(Post.created_at.desc()).all()
    
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'content_excerpt': post.content_excerpt,
            'author_id': post.author_id,
            'author_username': post.author.username,
            'category_id': post.category_id,
            'category_name': post.category.name,
            'created_at': post.created_at.isoformat()
        })
    
    return jsonify(posts_data)

@admin_bp.route('/posts/<int:post_id>/approve', methods=['POST'])
@admin_required
def approve_post_api(post_id):
    post = approve_post(post_id)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'status': post.status
    })

@admin_bp.route('/posts/<int:post_id>/reject', methods=['POST'])
@admin_required
def reject_post_api(post_id):
    data = request.json
    reason = data.get('reason', '')
    
    post = reject_post(post_id, reason)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'status': post.status
    })
