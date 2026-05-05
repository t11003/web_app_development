import sqlite3
import os
import logging

# 預設資料庫路徑 (對應到 instance/database.db)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

# 設定基本的 logging 記錄錯誤
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_db_connection():
    """取得資料庫連線"""
    try:
        # 確保 instance 資料夾存在
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # 讓查詢結果可以像字典一樣存取欄位
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def init_db():
    """初始化資料庫與資料表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            conn = get_db_connection()
            conn.executescript(schema_sql)
            conn.commit()
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
        finally:
            if 'conn' in locals() and conn:
                conn.close()

class RecordModel:
    @staticmethod
    def create(record_type, amount, date, category='', description=''):
        """新增一筆收支紀錄"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO records (type, amount, date, category, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (record_type, amount, date, category, description))
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except sqlite3.Error as e:
            logger.error(f"Error creating record: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得所有收支紀錄 (依日期遞減排序)"""
        conn = None
        try:
            conn = get_db_connection()
            records = conn.execute('''
                SELECT * FROM records ORDER BY date DESC, id DESC
            ''').fetchall()
            return [dict(row) for row in records]
        except sqlite3.Error as e:
            logger.error(f"Error getting all records: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(record_id):
        """根據 ID 取得單筆紀錄"""
        conn = None
        try:
            conn = get_db_connection()
            record = conn.execute('''
                SELECT * FROM records WHERE id = ?
            ''', (record_id,)).fetchone()
            return dict(record) if record else None
        except sqlite3.Error as e:
            logger.error(f"Error getting record by id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(record_id, record_type, amount, date, category='', description=''):
        """更新單筆收支紀錄"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE records 
                SET type = ?, amount = ?, date = ?, category = ?, description = ?
                WHERE id = ?
            ''', (record_type, amount, date, category, description, record_id))
            conn.commit()
            updated_rows = cursor.rowcount
            return updated_rows > 0
        except sqlite3.Error as e:
            logger.error(f"Error updating record: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(record_id):
        """刪除單筆收支紀錄"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM records WHERE id = ?
            ''', (record_id,))
            conn.commit()
            deleted_rows = cursor.rowcount
            return deleted_rows > 0
        except sqlite3.Error as e:
            logger.error(f"Error deleting record: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_balance():
        """計算目前總餘額"""
        conn = None
        try:
            conn = get_db_connection()
            result = conn.execute('''
                SELECT 
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) - 
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as balance
                FROM records
            ''').fetchone()
            return result['balance'] or 0
        except sqlite3.Error as e:
            logger.error(f"Error calculating balance: {e}")
            return 0
        finally:
            if conn:
                conn.close()
