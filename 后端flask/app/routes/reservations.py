from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.reservation import Reservation
from app.models.book import Book
from app.models.member import Member
from app.models.borrow import Borrow
from app.utils.auth import admin_required, login_required
from datetime import datetime, timedelta

bp = Blueprint('reservations', __name__)

@bp.route('/reservations', methods=['POST'])
@login_required
def create_reservation():
    """普通用户创建预约"""
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        
        if not book_id:
            return jsonify({'error': '图书ID为必填项'}), 400
        
        # 获取当前用户ID
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        
        # 检查图书是否存在
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': '图书不存在'}), 404
        
        # 检查用户是否存在
        member = Member.query.get(current_user_id)
        if not member:
            return jsonify({'error': '用户不存在'}), 404
        
        # 检查是否已经有未完成的预约
        existing_reservation = Reservation.query.filter_by(
            book_id=book_id, 
            member_id=current_user_id,
            status='pending'
        ).first()
        
        if existing_reservation:
            return jsonify({'error': '您已经预约了该图书'}), 400
        
        # 检查是否已经有借阅记录
        existing_borrow = Borrow.query.filter_by(
            book_id=book_id, 
            member_id=current_user_id,
            status='borrowed'
        ).first()
        
        if existing_borrow:
            return jsonify({'error': '您已经借阅了该图书'}), 400
        
        # 设置预约过期时间（7天后）
        expiry_date = datetime.utcnow() + timedelta(days=7)
        
        reservation = Reservation(
            book_id=book_id,
            member_id=current_user_id,
            expiry_date=expiry_date
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify({
            'message': '预约成功',
            'reservation': reservation.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/reservations', methods=['GET'])
@login_required
def get_reservations():
    """获取预约列表（管理员查看所有，普通用户查看自己的）"""
    try:
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        
        # 获取查询参数
        status = request.args.get('status', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 构建查询
        query = Reservation.query
        
        # 普通用户只能查看自己的预约
        from app.utils.auth import is_admin
        if not is_admin():
            query = query.filter_by(member_id=current_user_id)
        
        # 状态过滤
        if status:
            query = query.filter_by(status=status)
        
        # 分页
        reservations = query.order_by(Reservation.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reservations': [r.to_dict() for r in reservations.items],
            'total': reservations.total,
            'pages': reservations.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reservations/my-reservations', methods=['GET'])
@login_required
def get_my_reservations():
    """获取当前用户的预约列表"""
    try:
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        
        # 获取查询参数
        status = request.args.get('status', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 构建查询 - 只查询当前用户的预约
        query = Reservation.query.filter_by(member_id=current_user_id)
        
        # 状态过滤
        if status:
            query = query.filter_by(status=status)
        
        # 分页
        reservations = query.order_by(Reservation.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'reservations': [r.to_dict() for r in reservations.items],
            'total': reservations.total,
            'pages': reservations.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reservations/<int:reservation_id>', methods=['GET'])
@login_required
def get_reservation(reservation_id):
    """获取单个预约详情"""
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        
        # 权限检查：普通用户只能查看自己的预约
        from flask_jwt_extended import get_jwt_identity
        from app.utils.auth import is_admin
        current_user_id = get_jwt_identity()
        
        if not is_admin() and reservation.member_id != current_user_id:
            return jsonify({'error': '无权访问该预约'}), 403
        
        return jsonify(reservation.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reservations/<int:reservation_id>/approve', methods=['PUT'])
@admin_required
def approve_reservation(reservation_id):
    """管理员批准预约"""
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        
        if reservation.status != 'pending':
            return jsonify({'error': '只能批准待处理的预约'}), 400
        
        if reservation.is_expired():
            return jsonify({'error': '预约已过期'}), 400
        
        if reservation.book.available_copies <= 0:
            return jsonify({'error': '图书暂无可用副本'}), 400
        
        # 更新预约状态
        reservation.status = 'approved'
        
        # 创建借阅记录
        borrow_date = datetime.utcnow()
        due_date = borrow_date + timedelta(days=30)  # 借阅30天
        
        borrow = Borrow(
            book_id=reservation.book_id,
            member_id=reservation.member_id,
            borrow_date=borrow_date,
            due_date=due_date,
            status='borrowed'
        )
        
        db.session.add(borrow)
        
        # 更新预约完成时间
        reservation.completed_date = datetime.utcnow()
        reservation.status = 'completed'
        
        # 更新图书可用数量
        reservation.book.update_available_copies()
        
        db.session.commit()
        
        return jsonify({
            'message': '预约已批准并完成借阅',
            'reservation': reservation.to_dict(),
            'borrow': borrow.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/reservations/<int:reservation_id>/cancel', methods=['PUT'])
@login_required
def cancel_reservation(reservation_id):
    """取消预约"""
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        
        # 权限检查
        from flask_jwt_extended import get_jwt_identity
        from app.utils.auth import is_admin
        current_user_id = get_jwt_identity()
        
        # 将字符串ID转换为整数进行比较
        if not is_admin() and reservation.member_id != int(current_user_id):
            return jsonify({'error': '无权取消该预约'}), 403
        
        if reservation.status not in ['pending', 'approved']:
            return jsonify({'error': '只能取消待处理或已批准的预约'}), 400
        
        # 更新预约状态
        reservation.status = 'cancelled'
        reservation.cancelled_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': '预约已取消',
            'reservation': reservation.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/reservations/expired', methods=['POST'])
@admin_required
def cleanup_expired_reservations():
    """清理过期预约"""
    try:
        expired_reservations = Reservation.query.filter(
            Reservation.status == 'pending',
            Reservation.expiry_date < datetime.utcnow()
        ).all()
        
        for reservation in expired_reservations:
            reservation.status = 'cancelled'
            reservation.cancelled_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'已清理 {len(expired_reservations)} 个过期预约',
            'cleaned_count': len(expired_reservations)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500