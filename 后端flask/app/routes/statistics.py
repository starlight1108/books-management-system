from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.book import Book
from app.models.member import Member
from app.models.borrow import Borrow
from datetime import datetime, timedelta

bp = Blueprint('statistics', __name__)

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    try:
        # 基础统计
        total_books = Book.query.count()
        total_members = Member.query.count()
        borrowed_books = Borrow.query.filter_by(status='borrowed').count()
        available_books = db.session.query(Book).filter(Book.available_copies > 0).count()
        
        # 逾期统计
        overdue_books = Borrow.query.filter(
            Borrow.status == 'borrowed',
            Borrow.due_date < datetime.utcnow()
        ).count()
        
        # 今日统计
        today = datetime.utcnow().date()
        today_borrows = Borrow.query.filter(
            db.func.date(Borrow.borrow_date) == today
        ).count()
        
        today_returns = Borrow.query.filter(
            Borrow.status == 'returned',
            db.func.date(Borrow.return_date) == today
        ).count()
        
        # 分类统计
        category_stats = db.session.query(
            Book.category,
            db.func.count(Book.id).label('count')
        ).group_by(Book.category).all()
        
        category_data = {}
        for category, count in category_stats:
            category_name = category if category else '未分类'
            category_data[category_name] = count
        
        # 借阅趋势（最近7天）
        seven_days_ago = datetime.utcnow().date() - timedelta(days=7)
        borrow_trend = db.session.query(
            db.func.date(Borrow.borrow_date).label('date'),
            db.func.count(Borrow.id).label('count')
        ).filter(
            db.func.date(Borrow.borrow_date) >= seven_days_ago
        ).group_by(db.func.date(Borrow.borrow_date)).all()
        
        trend_data = {}
        for date, count in borrow_trend:
            # 确保日期是字符串格式
            date_str = str(date) if date else None
            if date_str:
                trend_data[date_str] = count
        
        # 热门图书（借阅次数最多的图书）
        popular_books = db.session.query(
            Book.title,
            db.func.count(Borrow.id).label('borrow_count')
        ).join(Borrow).group_by(Book.id).order_by(db.desc('borrow_count')).limit(5).all()
        
        popular_books_data = [
            {'title': title, 'borrow_count': count}
            for title, count in popular_books
        ]
        
        # 活跃会员（借阅次数最多的会员）
        active_members = db.session.query(
            Member.name,
            db.func.count(Borrow.id).label('borrow_count')
        ).join(Borrow).group_by(Member.id).order_by(db.desc('borrow_count')).limit(5).all()
        
        active_members_data = [
            {'name': name, 'borrow_count': count}
            for name, count in active_members
        ]
        
        statistics = {
            'total_books': total_books,
            'total_members': total_members,
            'borrowed_books': borrowed_books,
            'available_books': available_books,
            'overdue_books': overdue_books,
            'today_borrows': today_borrows,
            'today_returns': today_returns,
            'category_stats': category_data,
            'borrow_trend': trend_data,
            'popular_books': popular_books_data,
            'active_members': active_members_data
        }
        
        return jsonify(statistics), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics/overview', methods=['GET'])
def get_overview():
    try:
        # 月度统计
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        
        monthly_borrows = Borrow.query.filter(
            db.extract('month', Borrow.borrow_date) == current_month,
            db.extract('year', Borrow.borrow_date) == current_year
        ).count()
        
        monthly_returns = Borrow.query.filter(
            Borrow.status == 'returned',
            db.extract('month', Borrow.return_date) == current_month,
            db.extract('year', Borrow.return_date) == current_year
        ).count()
        
        # 会员增长趋势（最近6个月）
        six_months_ago = datetime.utcnow().date() - timedelta(days=180)
        member_growth = db.session.query(
            db.func.year(Member.join_date).label('year'),
            db.func.month(Member.join_date).label('month'),
            db.func.count(Member.id).label('count')
        ).filter(
            db.func.date(Member.join_date) >= six_months_ago
        ).group_by(db.func.year(Member.join_date), db.func.month(Member.join_date)).all()
        
        growth_data = {}
        for year, month, count in member_growth:
            month_key = f"{year}-{month:02d}"
            growth_data[month_key] = count
        
        overview = {
            'monthly_borrows': monthly_borrows,
            'monthly_returns': monthly_returns,
            'member_growth': growth_data
        }
        
        return jsonify(overview), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500