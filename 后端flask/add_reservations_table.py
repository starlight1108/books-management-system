#!/usr/bin/env python3
"""
添加预约表到数据库的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.reservation import Reservation

def add_reservations_table():
    """创建预约表"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建表
            db.create_all()
            print("✅ 预约表创建成功")
            
            # 检查表是否创建成功
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            if 'reservations' in tables:
                print("✅ reservations表已成功添加到数据库")
            else:
                print("❌ reservations表创建失败")
                
        except Exception as e:
            print(f"❌ 创建预约表时出错: {e}")

if __name__ == '__main__':
    add_reservations_table()