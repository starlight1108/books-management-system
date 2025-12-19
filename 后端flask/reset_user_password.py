from app import create_app
from app.extensions import db
from app.models.member import Member

# 创建应用上下文
app = create_app()

with app.app_context():
    # 重置李四的密码为123456
    user = Member.query.filter_by(name='李四').first()
    
    if user:
        user.set_password('123456')
        db.session.commit()
        print(f'成功重置用户 {user.name} (ID: {user.id}) 的密码为 "123456"')
    else:
        print('未找到用户 "李四"')
        
    # 查看当前所有用户的状态
    print('\n当前所有用户状态:')
    users = Member.query.all()
    for u in users:
        print(f'ID: {u.id}, 姓名: {u.name}, 角色: {u.role}, 状态: {u.status}')