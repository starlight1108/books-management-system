from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "library.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据模型
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    publisher = db.Column(db.String(100))
    publish_date = db.Column(db.Date)
    category = db.Column(db.String(50))
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    membership_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

class BorrowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    borrow_date = db.Column(db.Date, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='borrowed')
    
    book = db.relationship('Book', backref='borrow_records')
    member = db.relationship('Member', backref='borrow_records')

# 创建数据库表
with app.app_context():
    db.create_all()

# 图书管理API
@app.route('/api/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Book.query
    
    if search:
        query = query.filter(Book.title.contains(search) | Book.author.contains(search))
    
    if category:
        query = query.filter(Book.category == category)
    
    books = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'books': [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'publisher': book.publisher,
            'publish_date': book.publish_date.isoformat() if book.publish_date else None,
            'category': book.category,
            'total_copies': book.total_copies,
            'available_copies': book.available_copies,
            'description': book.description,
            'created_at': book.created_at.isoformat(),
            'updated_at': book.updated_at.isoformat()
        } for book in books.items],
        'total': books.total,
        'pages': books.pages,
        'current_page': books.page
    })

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    
    book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data.get('isbn'),
        publisher=data.get('publisher'),
        publish_date=datetime.fromisoformat(data['publish_date']) if data.get('publish_date') else None,
        category=data.get('category'),
        total_copies=data.get('total_copies', 1),
        available_copies=data.get('total_copies', 1),
        description=data.get('description')
    )
    
    try:
        db.session.add(book)
        db.session.commit()
        return jsonify({'message': '图书添加成功', 'book_id': book.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.publisher = data.get('publisher', book.publisher)
    book.publish_date = datetime.fromisoformat(data['publish_date']) if data.get('publish_date') else book.publish_date
    book.category = data.get('category', book.category)
    book.description = data.get('description', book.description)
    
    if 'total_copies' in data:
        book.total_copies = data['total_copies']
        # 重新计算可用副本数
        borrowed_count = BorrowRecord.query.filter_by(book_id=book_id, status='borrowed').count()
        book.available_copies = max(0, book.total_copies - borrowed_count)
    
    try:
        db.session.commit()
        return jsonify({'message': '图书更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    # 检查是否有未归还的借阅记录
    active_borrows = BorrowRecord.query.filter_by(book_id=book_id, status='borrowed').count()
    if active_borrows > 0:
        return jsonify({'error': '该图书有未归还的记录，无法删除'}), 400
    
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': '图书删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# 会员管理API
@app.route('/api/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{
        'id': member.id,
        'name': member.name,
        'email': member.email,
        'phone': member.phone,
        'address': member.address,
        'membership_date': member.membership_date.isoformat(),
        'status': member.status
    } for member in members])

@app.route('/api/members', methods=['POST'])
def add_member():
    data = request.get_json()
    
    member = Member(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address')
    )
    
    try:
        db.session.add(member)
        db.session.commit()
        return jsonify({'message': '会员添加成功', 'member_id': member.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# 借阅管理API
@app.route('/api/borrows', methods=['GET'])
def get_borrows():
    borrows = BorrowRecord.query.join(Book).join(Member).all()
    return jsonify([{
        'id': borrow.id,
        'book_id': borrow.book_id,
        'book_title': borrow.book.title,
        'member_id': borrow.member_id,
        'member_name': borrow.member.name,
        'borrow_date': borrow.borrow_date.isoformat(),
        'due_date': borrow.due_date.isoformat(),
        'return_date': borrow.return_date.isoformat() if borrow.return_date else None,
        'status': borrow.status
    } for borrow in borrows])

@app.route('/api/borrows', methods=['POST'])
def borrow_book():
    data = request.get_json()
    
    book_id = data['book_id']
    member_id = data['member_id']
    due_date = datetime.fromisoformat(data['due_date'])
    
    # 检查图书是否可借
    book = Book.query.get_or_404(book_id)
    if book.available_copies <= 0:
        return jsonify({'error': '该图书暂无可用副本'}), 400
    
    # 检查会员是否存在且状态正常
    member = Member.query.get_or_404(member_id)
    if member.status != 'active':
        return jsonify({'error': '该会员状态异常'}), 400
    
    # 检查会员是否已借阅该图书
    existing_borrow = BorrowRecord.query.filter_by(
        book_id=book_id, 
        member_id=member_id, 
        status='borrowed'
    ).first()
    
    if existing_borrow:
        return jsonify({'error': '该会员已借阅此图书'}), 400
    
    borrow_record = BorrowRecord(
        book_id=book_id,
        member_id=member_id,
        due_date=due_date
    )
    
    try:
        db.session.add(borrow_record)
        book.available_copies -= 1
        db.session.commit()
        return jsonify({'message': '借阅成功', 'borrow_id': borrow_record.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/borrows/<int:borrow_id>/return', methods=['PUT'])
def return_book(borrow_id):
    borrow_record = BorrowRecord.query.get_or_404(borrow_id)
    
    if borrow_record.status == 'returned':
        return jsonify({'error': '该图书已归还'}), 400
    
    try:
        borrow_record.status = 'returned'
        borrow_record.return_date = datetime.utcnow()
        borrow_record.book.available_copies += 1
        db.session.commit()
        return jsonify({'message': '归还成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# 统计API
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    total_books = Book.query.count()
    total_members = Member.query.count()
    borrowed_books = BorrowRecord.query.filter_by(status='borrowed').count()
    overdue_books = BorrowRecord.query.filter(
        BorrowRecord.status == 'borrowed',
        BorrowRecord.due_date < datetime.utcnow().date()
    ).count()
    
    return jsonify({
        'total_books': total_books,
        'total_members': total_members,
        'borrowed_books': borrowed_books,
        'available_books': total_books - borrowed_books,
        'overdue_books': overdue_books
    })

if __name__ == '__main__':
    app.run(debug=True)