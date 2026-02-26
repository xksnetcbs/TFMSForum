from flask import Blueprint, request, jsonify
from app.models import Post, PostStatus
from app.services.post_service import create_post, approve_post, reject_post, get_posts
from .auth import login_required, admin_required

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

@posts_bp.route('', methods=['POST'])
@login_required
def create_post_api():
    data = request.json
    title = data.get('title')
    content_markdown = data.get('content_markdown')
    category_id = data.get('category_id')
    
    if not title or not content_markdown or not category_id:
        return jsonify({'error': '缺少必要参数'}), 400
    
    from flask import session
    author_id = session['user_id']
    
    post = create_post(title, content_markdown, category_id, author_id)
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content_markdown': post.content_markdown,
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
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content_markdown': post.content_markdown,
        'author_id': post.author_id,
        'author_username': post.author.username,
        'category_id': post.category_id,
        'category_name': post.category.name,
        'status': post.status,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat()
    })
