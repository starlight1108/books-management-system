from app import create_app
from app.extensions import db
from app.models.member import Member

app = create_app()
with app.app_context():
    print('管理员用户:')
    for member in Member.query.filter_by(role='admin').all():
        print(f'  {member.name} (ID: {member.id}, 状态: {member.status})')
    
    print('\n普通用户:')
    for member in Member.query.filter_by(role='user').all():
        print(f'  {member.name} (ID: {member.id}, 状态: {member.status})')