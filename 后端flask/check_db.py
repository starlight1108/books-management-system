#!/usr/bin/env python
"""
检查数据库结构脚本
"""

import sqlite3
import os

def check_database():
    # 数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 获取所有表
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = cursor.fetchall()
        print('当前数据库中的表：')
        for table in tables:
            print(f'  - {table[0]}')
            
            # 显示表结构
            cursor.execute(f'PRAGMA table_info({table[0]})')
            columns = cursor.fetchall()
            print(f'    表结构：')
            for col in columns:
                print(f'      {col[1]} ({col[2]})')
            print()
            
    except Exception as e:
        print(f"检查数据库时出错: {e}")
        
    finally:
        # 关闭连接
        conn.close()

if __name__ == '__main__':
    check_database()