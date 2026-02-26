from flask import Blueprint, request, jsonify
from app.models import Post, User
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

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.order_by(User.id).all()
    
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'real_name': user.real_name,
            'student_id': user.student_id,
            'admission_year': user.admission_year,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat()
        })
    
    return jsonify(users_data)

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    data = request.json
    user.real_name = data.get('real_name', user.real_name)
    user.student_id = data.get('student_id', user.student_id)
    user.admission_year = data.get('admission_year', user.admission_year)
    user.is_admin = data.get('is_admin', user.is_admin)
    
    from app import db
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'real_name': user.real_name,
        'student_id': user.student_id,
        'admission_year': user.admission_year,
        'is_admin': user.is_admin
    })

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    from app import db
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': '用户已删除'})

