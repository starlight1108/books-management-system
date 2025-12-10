from app.extensions import db
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    join_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, inactive
    max_borrow_limit = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 与借阅记录的关系
    borrows = db.relationship('Borrow', backref='member', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'status': self.status,
            'max_borrow_limit': self.max_borrow_limit,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Member {self.name}>'