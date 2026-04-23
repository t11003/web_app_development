import sqlite3
import os
from contextlib import contextmanager

# 取得資料庫檔案存放的目錄 instance/ (位於專案根目錄)
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')

@contextmanager
def get_db_connection():
    # 若目錄不存在則建立一個
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 將回傳結果設為 dict-like 的 Row 物件
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

class Recipe:
    @staticmethod
    def create(data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes (title, description, ingredients, steps)
                VALUES (?, ?, ?, ?)
            ''', (data['title'], data.get('description', ''), data['ingredients'], data['steps']))
            return cursor.lastrowid
            
    @staticmethod
    def get_all(query=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if query:
                # 簡單支援對 title 或 ingredients 的 LIKE 搜尋 (搜尋推薦食譜)
                search_term = f"%{query}%"
                cursor.execute('''
                    SELECT * FROM recipes 
                    WHERE title LIKE ? OR ingredients LIKE ? 
                    ORDER BY created_at DESC
                ''', (search_term, search_term))
            else:
                cursor.execute('SELECT * FROM recipes ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
            
    @staticmethod
    def get_by_id(recipe_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
            
    @staticmethod
    def update(recipe_id, data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE recipes
                SET title = ?, description = ?, ingredients = ?, steps = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (data['title'], data.get('description', ''), data['ingredients'], data['steps'], recipe_id))
            return cursor.rowcount > 0

    @staticmethod
    def delete(recipe_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            return cursor.rowcount > 0
