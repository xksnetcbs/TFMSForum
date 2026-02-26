from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 基础配置
    app.config.from_object("app.config.Config")

    # 推迟导入模型，确保 db 已初始化
    from app import models  # noqa: F401

    # 初始化扩展
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "https://tfms.fback.dcpstudios.top"}}, supports_credentials=True)

    # 注册蓝图（后续在各模块中补充）
    from app.routes import register_routes

    register_routes(app)

    return app

