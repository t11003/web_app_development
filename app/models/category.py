from .db import get_db

class Category:
    @staticmethod
    def get_all():
        """取得所有分類"""
        conn = get_db()
        cursor = conn.execute('SELECT * FROM categories ORDER BY type, id')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(cat_id):
        """根據 ID 取得特定分類"""
        conn = get_db()
        cursor = conn.execute('SELECT * FROM categories WHERE id = ?', (cat_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create(name, type_, is_preset=0):
        """新增自訂分類"""
        conn = get_db()
        cursor = conn.execute(
            'INSERT INTO categories (name, type, is_preset) VALUES (?, ?, ?)',
            (name, type_, is_preset)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def update(cat_id, name):
        """更新分類名稱 (限自訂分類)"""
        conn = get_db()
        cursor = conn.execute(
            'UPDATE categories SET name = ? WHERE id = ? AND is_preset = 0',
            (name, cat_id)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0

    @staticmethod
    def delete(cat_id):
        """刪除分類 (檢查限自訂分類)"""
        conn = get_db()
        cursor = conn.execute('DELETE FROM categories WHERE id = ? AND is_preset = 0', (cat_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
