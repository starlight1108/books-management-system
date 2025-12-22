from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.review import Review
from app.models.book import Book
from app.models.member import Member
from app.utils.auth import self_or_admin_required
from datetime import datetime

bp = Blueprint('reviews', __name__)

@bp.route('/books/<int:book_id>/reviews', methods=['GET'])
def get_book_reviews(book_id):
    """获取某本书的所有评论"""
    try:
        # 验证书籍是否存在
        book = Book.query.get_or_404(book_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取评论，按创建时间倒序排列
        reviews_query = Review.query.filter_by(book_id=book_id).order_by(Review.created_at.desc())
        reviews = reviews_query.paginate(page=page, per_page=per_page, error_out=False)
        
        # 计算平均评分
        avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(book_id=book_id).scalar()
        avg_rating = round(avg_rating, 1) if avg_rating else 0
        
        # 统计各星级数量
        rating_counts = {}
        for i in range(1, 6):
            count = Review.query.filter_by(book_id=book_id, rating=i).count()
            rating_counts[str(i)] = count
        
        return jsonify({
            'book': book.to_dict(),
            'reviews': [review.to_dict() for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page,
            'average_rating': avg_rating,
            'rating_counts': rating_counts
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/books/<int:book_id>/reviews', methods=['POST'])
@jwt_required()
def add_review(book_id):
    """添加评论"""
    try:
        # 验证书籍是否存在
        book = Book.query.get_or_404(book_id)
        
        # 获取当前用户
        current_user_id = int(get_jwt_identity())
        current_user = Member.query.get(current_user_id)
        
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('rating') or not data.get('content'):
            return jsonify({'error': '评分和评论内容为必填项'}), 400
        
        # 验证评分范围
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': '评分必须在1-5之间'}), 400
        
        # 检查用户是否已经评论过这本书
        existing_review = Review.query.filter_by(book_id=book_id, member_id=current_user_id).first()
        if existing_review:
            return jsonify({'error': '您已经评论过这本书了'}), 400
        
        # 创建评论
        review = Review(
            book_id=book_id,
            member_id=current_user_id,
            rating=rating,
            content=data['content'].strip()
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify(review.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """修改评论"""
    try:
        review = Review.query.get_or_404(review_id)
        
        # 获取当前用户
        current_user_id = int(get_jwt_identity())
        current_user = Member.query.get(current_user_id)
        
        # 检查权限：只能修改自己的评论，或者管理员可以修改任何评论
        if review.member_id != current_user_id and current_user.role != 'admin':
            return jsonify({'error': '没有权限修改此评论'}), 403
        
        data = request.get_json()
        
        # 更新字段
        if 'rating' in data:
            rating = data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return jsonify({'error': '评分必须在1-5之间'}), 400
            review.rating = rating
        
        if 'content' in data:
            review.content = data['content'].strip()
        
        db.session.commit()
        
        return jsonify(review.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """删除评论"""
    try:
        review = Review.query.get_or_404(review_id)
        
        # 获取当前用户
        current_user_id = int(get_jwt_identity())
        current_user = Member.query.get(current_user_id)
        
        # 检查权限：只能删除自己的评论，或者管理员可以删除任何评论
        if review.member_id != current_user_id and current_user.role != 'admin':
            return jsonify({'error': '没有权限删除此评论'}), 403
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'message': '评论删除成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/members/<int:member_id>/reviews', methods=['GET'])
@self_or_admin_required
def get_member_reviews(member_id):
    """获取某个会员的所有评论"""
    try:
        member = Member.query.get_or_404(member_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        reviews_query = Review.query.filter_by(member_id=member_id).order_by(Review.created_at.desc())
        reviews = reviews_query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'member': member.to_dict(),
            'reviews': [review.to_dict() for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reviews/my-reviews', methods=['GET'])
@jwt_required()
def get_my_reviews():
    """获取当前用户的评论"""
    try:
        current_user_id = int(get_jwt_identity())
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        reviews_query = Review.query.filter_by(member_id=current_user_id).order_by(Review.created_at.desc())
        reviews = reviews_query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'reviews': [review.to_dict() for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500