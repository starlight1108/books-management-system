from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100))
    publish_date = db.Column(db.Date)
    category = db.Column(db.String(50))
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 与借阅记录的关系
    borrows = db.relationship('Borrow', backref='book', lazy=True)
    
    def get_borrowed_count(self):
        """获取当前借阅中的图书数量"""
        from app.models.borrow import Borrow
        return Borrow.query.filter_by(book_id=self.id, status='borrowed').count()
    
    def update_available_copies(self):
        """更新可借阅数：总册数 - 已借阅数"""
        borrowed_count = self.get_borrowed_count()
        self.available_copies = max(0, self.total_copies - borrowed_count)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None,
            'category': self.category,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'location': self.location,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Book {self.title}>'