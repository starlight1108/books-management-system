from app import create_app
from app.extensions import db
from app.models.member import Member

# 创建应用上下文
app = create_app()

with app.app_context():
    # 获取所有普通用户
    users = Member.query.filter_by(role='user').all()
    
    # 重置所有普通用户的密码为123456
    reset_count = 0
    for user in users:
        user.set_password('123456')
        reset_count += 1
    
    # 提交更改
    db.session.commit()
    
    print(f'已成功重置 {reset_count} 个普通用户的密码为 "123456"')
    
    # 显示所有用户信息
    print('\n所有用户信息:')
    all_users = Member.query.all()
    for user in all_users:
        print(f'ID: {user.id}, 姓名: {user.name}, 角色: {user.role}, 状态: {user.status}')