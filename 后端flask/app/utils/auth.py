from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.member import Member

def login_required(f):
    """装饰器：验证用户是否已登录"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': '需要登录'}), 401
        return f(*args, **kwargs)
    return decorated_function

def is_admin():
    """检查当前用户是否为管理员"""
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return False
    
    user = Member.query.get(int(current_user_id))
    return user and user.role == 'admin'

def admin_required(f):
    """装饰器：验证用户是否为管理员"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': '需要登录'}), 401

        # 将字符串ID转换为整数
        user = Member.query.get(int(current_user_id))
        if not user or user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403

        return f(*args, **kwargs)
    return decorated_function

def self_or_admin_required(f):
    """装饰器：验证用户是否为本人或管理员"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': '需要登录'}), 401

        # 将字符串ID转换为整数
        current_user_id = int(current_user_id)

        # 获取路由中的member_id参数
        member_id = kwargs.get('member_id')
        if member_id:
            # 如果是查看其他用户的信息，需要验证是否为管理员
            if int(member_id) != current_user_id:
                user = Member.query.get(current_user_id)
                if not user or user.role != 'admin':
                    return jsonify({'error': '只能查看自己的信息'}), 403

        return f(*args, **kwargs)
    return decorated_function