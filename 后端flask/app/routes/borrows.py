from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.borrow import Borrow
from app.models.book import Book
from app.models.member import Member
from datetime import datetime, timedelta

bp = Blueprint('borrows', __name__)

@bp.route('/borrows', methods=['GET'])
def get_borrows():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', '')
        overdue_only = request.args.get('overdue_only', 'false').lower() == 'true'
        
        query = Borrow.query
        
        # 状态过滤
        if status:
            query = query.filter(Borrow.status == status)
        
        # 逾期过滤
        if overdue_only:
            query = query.filter(
                Borrow.status == 'borrowed',
                Borrow.due_date < datetime.utcnow()
            )
        
        # 分页
        borrows = query.order_by(Borrow.borrow_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'borrows': [borrow.to_dict() for borrow in borrows.items],
            'total': borrows.total,
            'pages': borrows.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/borrows', methods=['POST'])
def borrow_book():
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('book_id') or not data.get('member_id'):
            return jsonify({'error': '图书ID和会员ID为必填项'}), 400
        
        book = Book.query.get_or_404(data['book_id'])
        member = Member.query.get_or_404(data['member_id'])
        
        # 检查图书是否可借
        if book.available_copies <= 0:
            return jsonify({'error': '该图书暂无库存'}), 400
        
        # 检查会员状态
        if member.status != 'active':
            return jsonify({'error': '会员状态异常，无法借阅'}), 400
        
        # 检查会员借阅上限
        current_borrows = Borrow.query.filter_by(
            member_id=member.id, status='borrowed'
        ).count()
        if current_borrows >= member.max_borrow_limit:
            return jsonify({'error': f'已达到最大借阅数量限制({member.max_borrow_limit}本)'}), 400
        
        # 计算应还日期（默认30天）
        borrow_date = datetime.utcnow()
        due_date = borrow_date + timedelta(days=data.get('borrow_days', 30))
        
        borrow = Borrow(
            book_id=book.id,
            member_id=member.id,
            borrow_date=borrow_date,
            due_date=due_date,
            status='borrowed'
        )
        
        # 更新图书库存
        book.available_copies -= 1
        
        db.session.add(borrow)
        db.session.commit()
        
        return jsonify(borrow.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/borrows/<int:borrow_id>/return', methods=['PUT'])
def return_book(borrow_id):
    try:
        borrow = Borrow.query.get_or_404(borrow_id)
        
        if borrow.status == 'returned':
            return jsonify({'error': '该图书已归还'}), 400
        
        # 更新借阅记录
        borrow.status = 'returned'
        borrow.return_date = datetime.utcnow()
        
        # 更新图书库存
        book = Book.query.get(borrow.book_id)
        if book:
            book.available_copies += 1
        
        db.session.commit()
        
        return jsonify(borrow.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/borrows/<int:borrow_id>', methods=['PUT'])
def update_borrow(borrow_id):
    try:
        borrow = Borrow.query.get_or_404(borrow_id)
        data = request.get_json()
        
        # 更新应还日期
        if 'due_date' in data:
            try:
                due_date = datetime.strptime(data['due_date'], '%Y-%m-%dT%H:%M:%S')
                borrow.due_date = due_date
            except ValueError:
                return jsonify({'error': '日期格式错误'}), 400
        
        # 更新状态
        if 'status' in data:
            borrow.status = data['status']
            if data['status'] == 'returned' and not borrow.return_date:
                borrow.return_date = datetime.utcnow()
                # 更新图书库存
                book = Book.query.get(borrow.book_id)
                if book:
                    book.available_copies += 1
        
        db.session.commit()
        
        return jsonify(borrow.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/borrows/<int:borrow_id>', methods=['DELETE'])
def delete_borrow(borrow_id):
    try:
        borrow = Borrow.query.get_or_404(borrow_id)
        
        # 如果是借阅中的记录，需要恢复图书库存
        if borrow.status == 'borrowed':
            book = Book.query.get(borrow.book_id)
            if book:
                book.available_copies += 1
        
        db.session.delete(borrow)
        db.session.commit()
        
        return jsonify({'message': '借阅记录删除成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/borrows/search', methods=['GET'])
def search_borrows():
    try:
        book_title = request.args.get('book_title', '')
        member_name = request.args.get('member_name', '')
        
        query = Borrow.query
        
        if book_title:
            query = query.join(Book).filter(Book.title.ilike(f'%{book_title}%'))
        
        if member_name:
            query = query.join(Member).filter(Member.name.ilike(f'%{member_name}%'))
        
        borrows = query.order_by(Borrow.borrow_date.desc()).limit(50).all()
        
        return jsonify({
            'borrows': [borrow.to_dict() for borrow in borrows]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500