from flask import Blueprint, Flask
from .auth import auth_bp
from .posts import posts_bp
from .comments import comments_bp
from .notifications import notifications_bp
from .categories import categories_bp
from .admin import admin_bp
from .likes import likes_bp
from .upload import upload_bp


def register_routes(app: Flask) -> None:
    """集中注册所有蓝图"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(likes_bp)
    app.register_blueprint(upload_bp)

