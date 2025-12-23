from app.extensions import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    
    # 预约状态：pending(等待处理), approved(已批准), completed(已完成), cancelled(已取消)
    status = db.Column(db.String(20), default='pending')
    
    # 预约时间
    reservation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 预约过期时间（预约保留期限）
    expiry_date = db.Column(db.DateTime)
    
    # 预约完成时间（当预约转为借阅时）
    completed_date = db.Column(db.DateTime)
    
    # 取消时间
    cancelled_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    book = db.relationship('Book', backref='reservations', lazy=True)
    member = db.relationship('Member', backref='reservations', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'book_title': self.book.title if self.book else None,
            'member_name': self.member.name if self.member else None,
            'status': self.status,
            'reservation_date': self.reservation_date.isoformat(),
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'cancelled_date': self.cancelled_date.isoformat() if self.cancelled_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def is_expired(self):
        """检查预约是否已过期"""
        if self.expiry_date and self.expiry_date < datetime.utcnow():
            return True
        return False
    
    def can_be_approved(self):
        """检查预约是否可以被批准"""
        return (self.status == 'pending' and 
                not self.is_expired() and 
                self.book.available_copies > 0)
    
    def __repr__(self):
        return f'<Reservation {self.id}>'