from .database import get_db_connection

class Donation:
    @staticmethod
    def create(user_id, amount, status='completed'):
        """
        新增一筆隨喜捐款紀錄
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO donations (user_id, amount, status) VALUES (?, ?, ?)',
                (user_id, amount, status)
            )
            conn.commit()
            don_id = cursor.lastrowid
            conn.close()
            return don_id
        except Exception as e:
            print(f"Error creating donation: {e}")
            return None

    @staticmethod
    def get_by_user_id(user_id):
        """取得某會員的歷史隨喜紀錄"""
        try:
            conn = get_db_connection()
            dons = conn.execute('SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
            conn.close()
            return [dict(d) for d in dons]
        except Exception as e:
            print(f"Error getting donations for user: {e}")
            return []
