from app import create_app, db  # type: ignore


def init_db() -> None:
    app = create_app()
    with app.app_context():
        # 先删除所有表，然后重新创建，确保表结构更新
        db.drop_all()
        db.create_all()
        print("Database tables dropped and recreated.")


if __name__ == "__main__":
    init_db()

