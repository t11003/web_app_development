from .database import get_db_connection

class Divination:
    @staticmethod
    def create(user_id, div_type, question, result, explanation):
        """
        新增一筆占卜紀錄
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO divinations (user_id, type, question, result, explanation) VALUES (?, ?, ?, ?, ?)',
                (user_id, div_type, question, result, explanation)
            )
            conn.commit()
            div_id = cursor.lastrowid
            conn.close()
            return div_id
        except Exception as e:
            print(f"Error creating divination: {e}")
            return None

    @staticmethod
    def get_by_id(div_id):
        """取得單一紀錄"""
        try:
            conn = get_db_connection()
            div = conn.execute('SELECT * FROM divinations WHERE id = ?', (div_id,)).fetchone()
            conn.close()
            return dict(div) if div else None
        except Exception as e:
            print(f"Error getting divination: {e}")
            return None

    @staticmethod
    def get_by_user_id(user_id):
        """取得某會員的所有占卜紀錄"""
        try:
            conn = get_db_connection()
            divs = conn.execute('SELECT * FROM divinations WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
            conn.close()
            return [dict(d) for d in divs]
        except Exception as e:
            print(f"Error getting divinations for user: {e}")
            return []

    @staticmethod
    def delete(div_id):
        """刪除占卜紀錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM divinations WHERE id = ?', (div_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting divination: {e}")
            return False
