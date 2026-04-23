import sqlite3
import os

# 自動推導 instance/expense.db 路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'expense.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    # 使用 sqlite3.Row 讓查詢結果能像 dictionary 那樣透過欄位名稱取值
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    conn = get_db()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
