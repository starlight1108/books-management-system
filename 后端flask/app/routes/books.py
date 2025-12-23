from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.book import Book
from datetime import datetime

bp = Blueprint('books', __name__)

@bp.route('/books', methods=['GET'])
def get_books():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        
        query = Book.query
        
        # 搜索过滤
        if search:
            query = query.filter(
                db.or_(
                    Book.title.ilike(f'%{search}%'),
                    Book.author.ilike(f'%{search}%'),
                    Book.isbn.ilike(f'%{search}%')
                )
            )
        
        # 分类过滤
        if category:
            query = query.filter(Book.category == category)
        
        # 分页
        books = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'books': [book.to_dict() for book in books.items],
            'total': books.total,
            'pages': books.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/books', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('title') or not data.get('author') or not data.get('isbn'):
            return jsonify({'error': '书名、作者和ISBN为必填项'}), 400
        
        # 检查ISBN是否已存在
        existing_book = Book.query.filter_by(isbn=data['isbn']).first()
        if existing_book:
            return jsonify({'error': 'ISBN已存在'}), 400
        
        # 处理出版日期
        publish_date = None
        if data.get('publish_date'):
            try:
                publish_date = datetime.strptime(data['publish_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '出版日期格式错误，应为YYYY-MM-DD'}), 400
        
        book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            publisher=data.get('publisher'),
            publish_date=publish_date,
            category=data.get('category'),
            total_copies=data.get('total_copies', 1),
            available_copies=data.get('total_copies', 1),  # 新添加的图书，可借阅数等于总册数
            location=data.get('location'),
            description=data.get('description')
        )
        
        db.session.add(book)
        db.session.commit()
        
        return jsonify(book.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        
        # 更新字段
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'publisher' in data:
            book.publisher = data['publisher']
        if 'category' in data:
            book.category = data['category']
        if 'total_copies' in data:
            book.total_copies = data['total_copies']
            # 修改总册数时，自动更新可借阅数
            book.update_available_copies()
        if 'location' in data:
            book.location = data['location']
        if 'description' in data:
            book.description = data['description']
        
        # 更新ISBN并验证唯一性
        if 'isbn' in data:
            new_isbn = data['isbn']
            # 检查ISBN是否被其他图书使用
            existing_book = Book.query.filter_by(isbn=new_isbn).first()
            if existing_book and existing_book.id != book_id:
                return jsonify({'error': 'ISBN已存在'}), 400
            book.isbn = new_isbn
        
        # 处理出版日期
        if 'publish_date' in data:
            if data['publish_date']:
                try:
                    book.publish_date = datetime.strptime(data['publish_date'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': '出版日期格式错误，应为YYYY-MM-DD'}), 400
            else:
                book.publish_date = None
        
        db.session.commit()
        
        return jsonify(book.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        
        # 检查是否有借阅记录
        if book.borrows:
            return jsonify({'error': '该图书有借阅记录，无法删除'}), 400
        
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({'message': '图书删除成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/books/categories', methods=['GET'])
def get_categories():
    try:
        categories = db.session.query(Book.category).distinct().filter(Book.category.isnot(None)).all()
        category_list = [category[0] for category in categories if category[0]]
        return jsonify({'categories': category_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500