from app.extensions import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 评分 1-5
    content = db.Column(db.Text, nullable=False)  # 评论内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 与书籍和会员的关系
    book = db.relationship('Book', backref='reviews')
    member = db.relationship('Member', backref='reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'member_name': self.member.name if self.member else None,
            'rating': self.rating,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Review {self.id} for Book {self.book_id}>'