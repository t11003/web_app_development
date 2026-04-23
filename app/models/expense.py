from .db import get_db
from datetime import datetime

class Expense:
    @staticmethod
    def get_all():
        """取得所有收支紀錄 (包含分類名稱)"""
        conn = get_db()
        query = '''
            SELECT e.*, c.name as category_name, c.type as category_type
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            ORDER BY e.date DESC, e.created_at DESC
        '''
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(expense_id):
        """根據 ID 取得單筆收支明細"""
        conn = get_db()
        query = '''
            SELECT e.*, c.name as category_name, c.type as category_type
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.id = ?
        '''
        cursor = conn.execute(query, (expense_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create(amount, category_id, note, date):
        """新增一筆收支紀錄"""
        conn = get_db()
        created_at = datetime.now().isoformat()
        cursor = conn.execute(
            'INSERT INTO expenses (amount, category_id, note, date, created_at) VALUES (?, ?, ?, ?, ?)',
            (amount, category_id, note, date, created_at)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def update(expense_id, amount, category_id, note, date):
        """更新一筆收支紀錄"""
        conn = get_db()
        cursor = conn.execute(
            '''UPDATE expenses 
               SET amount = ?, category_id = ?, note = ?, date = ? 
               WHERE id = ?''',
            (amount, category_id, note, date, expense_id)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0

    @staticmethod
    def delete(expense_id):
        """刪除一筆收支紀錄"""
        conn = get_db()
        cursor = conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
