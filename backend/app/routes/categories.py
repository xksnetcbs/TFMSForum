from flask import Blueprint, jsonify
from app.models import Category

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
