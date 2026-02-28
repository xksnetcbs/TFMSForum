from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.log import log
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': '未登录'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': '未登录'}), 401
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({'error': '权限不足'}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    real_name = data.get('real_name')
    student_id = data.get('student_id')
    admission_year = data.get('admission_year')

    if not username or not email or not password:
        return jsonify({'error': '缺少必要参数'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': '邮箱已被注册'}), 400

    password_hash = generate_password_hash(password)
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        real_name=real_name,
        student_id=student_id,
        admission_year=admission_year
    )

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id

    log(f'用户 {username} 注册成功')

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'real_name': user.real_name,
        'student_id': user.student_id,
        'admission_year': user.admission_year,
        'is_admin': user.is_admin
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('identifier')  # 可以是用户名或邮箱
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'error': '缺少必要参数'}), 400

    # 尝试通过用户名查找
    user = User.query.filter_by(username=identifier).first()
    # 如果没找到，尝试通过邮箱查找
    if not user:
        user = User.query.filter_by(email=identifier).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': '用户名/邮箱或密码错误'}), 401

    session['user_id'] = user.id

    log(f'用户 {user.username} 上线了')

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'real_name': user.real_name,
        'student_id': user.student_id,
        'admission_year': user.admission_year,
        'is_admin': user.is_admin
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': '登出成功'})

@auth_bp.route('/me')
def get_current_user():
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401

    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return jsonify({'error': '用户不存在'}), 401

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'real_name': user.real_name,
        'student_id': user.student_id,
        'admission_year': user.admission_year,
        'is_admin': user.is_admin
    })

@auth_bp.route('/me', methods=['PUT'])
@login_required
def update_user_info():
    data = request.json
    real_name = data.get('real_name')
    student_id = data.get('student_id')
    admission_year = data.get('admission_year')

    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return jsonify({'error': '用户不存在'}), 401

    # 更新用户信息
    if real_name is not None:
        user.real_name = real_name
    if student_id is not None:
        user.student_id = student_id
    if admission_year is not None:
        user.admission_year = admission_year

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
