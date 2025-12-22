#!/usr/bin/env python
"""
添加评论表到数据库
"""

import sqlite3
import os

def add_reviews_table():
    # 数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查评论表是否已存在
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="reviews"')
        if cursor.fetchone():
            print("评论表已存在，无需创建")
            return
        
        # 创建评论表
        cursor.execute('''
            CREATE TABLE reviews (
                id INTEGER PRIMARY KEY,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (member_id) REFERENCES members (id)
            )
        ''')
        
        # 提交更改
        conn.commit()
        print("评论表创建成功！")
        
    except Exception as e:
        # 发生错误时回滚
        conn.rollback()
        print(f"创建评论表失败: {e}")
        
    finally:
        # 关闭连接
        conn.close()

if __name__ == '__main__':
    add_reviews_table()