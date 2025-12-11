#!/usr/bin/env python
"""
数据库更新脚本：修改members表结构
- 添加password_hash字段
- 将name字段设置为唯一
- 将email字段设置为可选
"""

import sqlite3
import os

def update_database():
    # 数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 创建临时表，结构与原表相同但添加password_hash字段，name字段唯一，email字段可选
        cursor.execute('''
            CREATE TABLE members_temp (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(120) UNIQUE,
                password_hash VARCHAR(128) NOT NULL DEFAULT '',
                phone VARCHAR(20),
                address TEXT,
                join_date DATE,
                status VARCHAR(20) DEFAULT 'active',
                max_borrow_limit INTEGER DEFAULT 5,
                created_at DATETIME,
                updated_at DATETIME
            )
        ''')
        
        # 2. 将原表数据复制到临时表
        cursor.execute('''
            INSERT INTO members_temp (
                id, name, email, phone, address, 
                join_date, status, max_borrow_limit, created_at, updated_at
            )
            SELECT 
                id, name, email, phone, address, 
                join_date, status, max_borrow_limit, created_at, updated_at
            FROM members
        ''')
        
        # 3. 删除原表
        cursor.execute('DROP TABLE members')
        
        # 4. 将临时表重命名为原表名
        cursor.execute('ALTER TABLE members_temp RENAME TO members')
        
        # 提交更改
        conn.commit()
        print("数据库更新成功！")
        
    except Exception as e:
        # 发生错误时回滚
        conn.rollback()
        print(f"数据库更新失败: {e}")
        
    finally:
        # 关闭连接
        conn.close()

if __name__ == '__main__':
    update_database()