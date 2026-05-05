import sqlite3
import os

# 預設資料庫路徑 (對應到 instance/database.db)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以像字典一樣存取欄位
    return conn

def init_db():
    """初始化資料庫與資料表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn = get_db_connection()
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()

class RecordModel:
    @staticmethod
    def create(record_type, amount, date, category='', description=''):
        """新增一筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO records (type, amount, date, category, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (record_type, amount, date, category, description))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        """取得所有收支紀錄 (依日期遞減排序)"""
        conn = get_db_connection()
        records = conn.execute('''
            SELECT * FROM records ORDER BY date DESC, id DESC
        ''').fetchall()
        conn.close()
        return [dict(row) for row in records]

    @staticmethod
    def get_by_id(record_id):
        """根據 ID 取得單筆紀錄"""
        conn = get_db_connection()
        record = conn.execute('''
            SELECT * FROM records WHERE id = ?
        ''', (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def update(record_id, record_type, amount, date, category='', description=''):
        """更新單筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE records 
            SET type = ?, amount = ?, date = ?, category = ?, description = ?
            WHERE id = ?
        ''', (record_type, amount, date, category, description, record_id))
        conn.commit()
        updated_rows = cursor.rowcount
        conn.close()
        return updated_rows > 0

    @staticmethod
    def delete(record_id):
        """刪除單筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM records WHERE id = ?
        ''', (record_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        conn.close()
        return deleted_rows > 0

    @staticmethod
    def get_balance():
        """計算目前總餘額"""
        conn = get_db_connection()
        result = conn.execute('''
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) - 
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as balance
            FROM records
        ''').fetchone()
        conn.close()
        return result['balance'] or 0
