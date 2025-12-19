from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.member import Member
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re

bp = Blueprint('auth', __name__)

# 密码验证（至少6位数字）
PASSWORD_REGEX = re.compile(r'^\d{6,}$')

@bp.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('name') or not data.get('password'):
            return jsonify({'error': '姓名和密码为必填项'}), 400
        
        # 验证密码格式
        if not PASSWORD_REGEX.match(data['password']):
            return jsonify({
                'error': '密码必须至少6位数字'
            }), 400
        
        # 检查用户名是否已存在
        existing_member = Member.query.filter_by(name=data['name']).first()
        if existing_member:
            return jsonify({'error': '用户名已存在'}), 400
        
        # 创建新会员
        member = Member(
            name=data['name'],
            phone=data.get('phone')
        )
        
        # 设置密码（自动进行哈希处理）
        member.set_password(data['password'])
        
        db.session.add(member)
        db.session.commit()
        
        # 创建访问令牌，identity需要是字符串类型
        access_token = create_access_token(identity=str(member.id))
        
        return jsonify({
            'message': '注册成功',
            'access_token': access_token,
            'user': {
                'id': member.id,
                'name': member.name,
                'role': member.role
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('name') or not data.get('password'):
            return jsonify({'error': '用户名和密码为必填项'}), 400
        
        # 查找用户
        member = Member.query.filter_by(name=data['name']).first()
        if not member or not member.check_password(data['password']):
            return jsonify({'error': '用户名或密码错误'}), 401
        
        # 检查用户状态
        if member.status != 'active':
            return jsonify({'error': '账户已被禁用，请联系管理员'}), 403
        
        # 创建访问令牌，identity需要是字符串类型
        access_token = create_access_token(identity=str(member.id))
        
        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'user': {
                'id': member.id,
                'name': member.name,
                'role': member.role
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        # 获取当前用户ID，并转换为整数类型
        current_user_id = int(get_jwt_identity())
        
        # 查询用户信息
        member = Member.query.get(current_user_id)
        if not member:
            return jsonify({'error': '用户不存在'}), 404
        
        return jsonify({
            'user': {
                'id': member.id,
                'name': member.name,
                'phone': member.phone,
                'join_date': member.join_date.isoformat() if member.join_date else None,
                'status': member.status,
                'role': member.role,
                'max_borrow_limit': member.max_borrow_limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        # 获取当前用户ID
        current_user_id = get_jwt_identity()
        
        # 获取请求数据
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        # 验证必填字段
        if not old_password or not new_password:
            return jsonify({'error': '旧密码和新密码为必填项'}), 400
        
        # 验证新密码格式
        if not PASSWORD_REGEX.match(new_password):
            return jsonify({
                'error': '新密码必须至少6位数字'
            }), 400
        
        # 查询用户
        member = Member.query.get(current_user_id)
        if not member:
            return jsonify({'error': '用户不存在'}), 404
        
        # 验证旧密码
        if not member.check_password(old_password):
            return jsonify({'error': '旧密码错误'}), 401
        
        # 设置新密码
        member.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': '密码修改成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500