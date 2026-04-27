import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立並回傳資料庫連線，設定 row_factory 讓結果可透過字典的 key 來存取。"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫實體，執行 schema.sql。"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        return
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    with get_db_connection() as conn:
        conn.executescript(schema)
