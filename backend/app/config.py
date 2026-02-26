import os


class Config:
    SECRET_KEY = os.environ.get("TFMSFORUM_SECRET_KEY", "dev-secret-key")

    # MySQL 数据库连接，示例：mysql+pymysql://user:password@localhost:3306/tfms_forum
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TFMSFORUM_DATABASE_URI",
        "mysql+pymysql://tfms_forum:tfmstfms@localhost:3306/tfms_forum",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 以后可以在这里扩展更多配置，如分页大小、上传目录等

