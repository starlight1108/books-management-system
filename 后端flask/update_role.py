from app.extensions import db
from app.models.member import Member
from sqlalchemy import text

def add_role_column():
    """为会员表添加角色字段"""
    try:
        # 添加角色列
        db.session.execute(text('ALTER TABLE members ADD COLUMN role VARCHAR(20) DEFAULT "user"'))
        db.session.commit()

        # 设置第一个用户为管理员（假设第一个注册的用户是管理员）
        first_user = Member.query.first()
        if first_user:
            first_user.role = 'admin'
            db.session.commit()
            print(f"已将用户 {first_user.name} 设置为管理员")

        print("角色字段添加成功")
        return True
    except Exception as e:
        print(f"添加角色字段失败: {str(e)}")
        return False

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        add_role_column()
