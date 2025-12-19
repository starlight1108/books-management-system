from app.extensions import db
from datetime import datetime
import bcrypt

class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # 添加唯一性约束
    email = db.Column(db.String(120), unique=True, nullable=True)  # 改为可选
    password_hash = db.Column(db.String(128), nullable=False)  # 添加密码哈希字段
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    join_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, inactive
    role = db.Column(db.String(20), default='user')  # user, admin
    max_borrow_limit = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 与借阅记录的关系
    borrows = db.relationship('Borrow', backref='member', lazy=True)
    
    def set_password(self, password):
        """设置密码，进行哈希处理"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        """验证密码"""
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'status': self.status,
            'role': self.role,
            'max_borrow_limit': self.max_borrow_limit,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Member {self.name}>'