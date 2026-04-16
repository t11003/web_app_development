import sqlite3
import os

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../instance/database.db')

def get_db_connection():
    """
    建立並回傳一個與 SQLite 資料庫的連線。
    預設啟用 row_factory 為 sqlite3.Row，以利透過字典鍵值存取資料。
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    """
    初始化資料庫。讀取 schema.sql 並執行建表語句。
    """
    try:
        conn = get_db_connection()
        schema_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../database/schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database initialization error: {e}")
