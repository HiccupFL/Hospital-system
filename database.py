import json
import os
import sqlite3
import sys
from datetime import datetime

class Database:
    def __init__(self, db_path=None):
        # 获取应用程序根目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的程序
            app_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            app_path = os.path.dirname(os.path.abspath(__file__))
        
        # 如果没有指定数据库路径，使用默认路径
        if db_path is None:
            self.db_path = os.path.join(app_path, 'data', 'medicines.db')
        else:
            self.db_path = db_path
            
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        # 确保数据目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 连接到数据库
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        # 创建药品表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            manufacturer TEXT,
            production_date TEXT,
            expiry_date TEXT,
            min_quantity INTEGER DEFAULT 0,
            current_quantity INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        )
        ''')
        self.conn.commit()
    
    def add_medicine(self, medicine):
        # 添加新药品
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
        INSERT INTO medicines (name, manufacturer, production_date, expiry_date, 
                              min_quantity, current_quantity, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            medicine['name'],
            medicine['manufacturer'],
            medicine['production_date'],
            medicine['expiry_date'],
            medicine['min_quantity'],
            medicine['current_quantity'],
            now,
            now
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_medicine(self, medicine):
        # 更新药品信息
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
        UPDATE medicines
        SET name = ?, manufacturer = ?, production_date = ?, expiry_date = ?,
            min_quantity = ?, current_quantity = ?, updated_at = ?
        WHERE id = ?
        ''', (
            medicine['name'],
            medicine['manufacturer'],
            medicine['production_date'],
            medicine['expiry_date'],
            medicine['min_quantity'],
            medicine['current_quantity'],
            now,
            medicine['id']
        ))
        self.conn.commit()
    
    def update_quantity(self, medicine_id, new_quantity):
        # 更新药品数量
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
        UPDATE medicines
        SET current_quantity = ?, updated_at = ?
        WHERE id = ?
        ''', (new_quantity, now, medicine_id))
        self.conn.commit()
    
    def delete_medicine(self, medicine_id):
        # 删除药品
        self.cursor.execute('DELETE FROM medicines WHERE id = ?', (medicine_id,))
        self.conn.commit()
        
    def get_all_medicines(self):
        # 获取所有药品
        self.cursor.execute('SELECT * FROM medicines ORDER BY name')
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_medicine_by_id(self, medicine_id):
        # 根据ID获取药品
        self.cursor.execute('SELECT * FROM medicines WHERE id = ?', (medicine_id,))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None

    def search_medicines(self, keyword):
        # 搜索药品
        self.cursor.execute('''
        SELECT * FROM medicines 
        WHERE name LIKE ? OR manufacturer LIKE ?
        ORDER BY name
        ''', (f'%{keyword}%', f'%{keyword}%'))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self):
        # 关闭数据库连接
        if self.conn:
            self.conn.close()