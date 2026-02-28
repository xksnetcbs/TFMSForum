from flask import Blueprint, request, jsonify, session
from app.models import Category
from app.log import log
from .auth import login_required, admin_required
from app import db

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@categories_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.order).all()
    categories_data = []
    for category in categories:
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'order': category.order
        })
    return jsonify(categories_data)

@categories_bp.route('', methods=['POST'])
@login_required
@admin_required
def create_category():
    data = request.json
    name = data.get('name')
    slug = data.get('slug')
    order = data.get('order', 0)
    
    if not name or not slug:
        return jsonify({'error': '缺少必要参数'}), 400
    
    # 检查分类名是否已存在
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({'error': '分类名已存在'}), 400
    
    # 检查slug是否已存在
    existing_slug = Category.query.filter_by(slug=slug).first()
    if existing_slug:
        return jsonify({'error': 'slug已存在'}), 400
    
    new_category = Category(name=name, slug=slug, order=order)
    db.session.add(new_category)
    db.session.commit()

    log(f'用户 {session["user_id"]} 创建了分类 {new_category.name}')

    return jsonify({
        'id': new_category.id,
        'name': new_category.name,
        'slug': new_category.slug,
        'order': new_category.order
    })

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@login_required
@admin_required
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': '分类不存在'}), 404
    
    data = request.json
    name = data.get('name')
    slug = data.get('slug')
    order = data.get('order')
    
    # 检查分类名是否已被其他分类使用
    if name and name != category.name:
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            return jsonify({'error': '分类名已存在'}), 400
        category.name = name
    
    # 检查slug是否已被其他分类使用
    if slug and slug != category.slug:
        existing_slug = Category.query.filter_by(slug=slug).first()
        if existing_slug:
            return jsonify({'error': 'slug已存在'}), 400
        category.slug = slug
    
    if order is not None:
        category.order = order
    
    db.session.commit()

    log(f'用户 {session["user_id"]} 更新了分类 {category.name}')
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'slug': category.slug,
        'order': category.order
    })

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': '分类不存在'}), 404
    
    # 检查是否有帖子属于该分类
    if category.posts.count() > 0:
        return jsonify({'error': '该分类下存在帖子，无法删除'}), 400
    
    db.session.delete(category)
    db.session.commit()

    log(f'用户 {session["user_id"]} 删除了分类 {category.name}')
    
    return jsonify({'message': '分类删除成功'})
