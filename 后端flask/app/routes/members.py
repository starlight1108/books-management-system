from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.member import Member
from app.models.borrow import Borrow
from app.utils.auth import admin_required, self_or_admin_required
from datetime import datetime

bp = Blueprint('members', __name__)

@bp.route('/members', methods=['GET'])
@admin_required
def get_members():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        
        query = Member.query
        
        # 搜索过滤
        if search:
            query = query.filter(
                db.or_(
                    Member.name.ilike(f'%{search}%'),
                    Member.email.ilike(f'%{search}%'),
                    Member.phone.ilike(f'%{search}%')
                )
            )
        
        # 状态过滤
        if status:
            query = query.filter(Member.status == status)
        
        # 分页
        members = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'members': [member.to_dict() for member in members.items],
            'total': members.total,
            'pages': members.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/members/<int:member_id>', methods=['GET'])
@self_or_admin_required
def get_member(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        
        # 获取会员的借阅记录
        borrows = Borrow.query.filter_by(member_id=member_id).all()
        member_data = member.to_dict()
        member_data['current_borrows'] = len([b for b in borrows if b.status == 'borrowed'])
        
        return jsonify(member_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/members', methods=['POST'])
@admin_required
def add_member():
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': '姓名、邮箱和密码为必填项'}), 400
        
        # 检查邮箱是否已存在
        existing_member = Member.query.filter_by(email=data['email']).first()
        if existing_member:
            return jsonify({'error': '邮箱已存在'}), 400
        
        # 处理入会日期
        join_date = None
        if data.get('join_date'):
            try:
                join_date = datetime.strptime(data['join_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '入会日期格式错误，应为YYYY-MM-DD'}), 400
        
        member = Member(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            address=data.get('address'),
            join_date=join_date,
            status=data.get('status', 'active'),
            max_borrow_limit=data.get('max_borrow_limit', 5)
        )
        
        # 设置密码
        member.set_password(data['password'])
        
        db.session.add(member)
        db.session.commit()
        
        return jsonify(member.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/members/<int:member_id>', methods=['PUT'])
@self_or_admin_required
def update_member(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        data = request.get_json()
        
        # 获取当前用户信息
        current_user_id = int(get_jwt_identity())
        current_user = Member.query.get(current_user_id)
        
        # 更新字段
        if 'name' in data:
            # 检查用户名是否重复
            if data['name'] != member.name:
                existing_member = Member.query.filter_by(name=data['name']).first()
                if existing_member:
                    return jsonify({'error': '用户名已存在'}), 400
            member.name = data['name']
        if 'phone' in data:
            member.phone = data['phone']
        if 'address' in data:
            member.address = data['address']
        
        # 只有管理员可以修改状态和借阅限制
        if current_user.role == 'admin':
            if 'status' in data:
                member.status = data['status']
            if 'max_borrow_limit' in data:
                member.max_borrow_limit = data['max_borrow_limit']
        
        # 检查邮箱是否重复
        if 'email' in data and data['email'] != member.email:
            existing_member = Member.query.filter_by(email=data['email']).first()
            if existing_member:
                return jsonify({'error': '邮箱已存在'}), 400
            member.email = data['email']
        
        # 处理入会日期
        if 'join_date' in data:
            if data['join_date']:
                try:
                    member.join_date = datetime.strptime(data['join_date'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': '入会日期格式错误，应为YYYY-MM-DD'}), 400
            else:
                member.join_date = None
        
        # 更新密码（如果提供）
        if 'password' in data:
            member.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify(member.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/members/<int:member_id>', methods=['DELETE'])
@admin_required
def delete_member(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        
        # 禁止删除管理员用户
        if member.role == 'admin':
            return jsonify({'error': '管理员用户无法删除'}), 400
        
        # 检查是否有未归还的借阅记录
        active_borrows = Borrow.query.filter_by(member_id=member_id, status='borrowed').count()
        if active_borrows > 0:
            return jsonify({'error': '该会员有未归还的图书，无法删除'}), 400
        
        # 删除相关的借阅记录
        Borrow.query.filter_by(member_id=member_id).delete()
        
        db.session.delete(member)
        db.session.commit()
        
        return jsonify({'message': '会员删除成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/members/<int:member_id>/borrows', methods=['GET'])
@self_or_admin_required
def get_member_borrows(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        
        borrows = Borrow.query.filter_by(member_id=member_id).order_by(Borrow.borrow_date.desc()).all()
        
        return jsonify({
            'member': member.to_dict(),
            'borrows': [borrow.to_dict() for borrow in borrows]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500