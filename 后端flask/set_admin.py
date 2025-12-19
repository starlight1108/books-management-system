#!/usr/bin/env python
"""
将指定用户设置为管理员
"""

from app import create_app
from app.models.member import Member
from app.extensions import db

app = create_app()

with app.app_context():
    # 查找用户
    user = Member.query.filter_by(name='starlight').first()
    
    if not user:
        print(f"错误：找不到用户 'starlight'")
    else:
        # 将用户角色设置为管理员
        user.role = 'admin'
        db.session.commit()
        print(f"成功：用户 '{user.name}' 已设置为管理员角色")
        print(f"用户信息：ID: {user.id}, 用户名: {user.name}, 角色: {user.role}, 状态: {user.status}")