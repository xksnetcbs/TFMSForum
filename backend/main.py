from app import create_app

app = create_app()


if __name__ == "__main__":
    # 开发环境运行
    app.run(host="0.0.0.0", port=5007, debug=True)

