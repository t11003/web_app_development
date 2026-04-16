from .database import get_db_connection

class User:
    @staticmethod
    def create(username, password_hash, is_admin=0):
        """
        新增一筆使用者記錄。
        回傳新建使用者的 id，發生例外時回傳 None。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)',
                (username, password_hash, is_admin)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        """
        根據 id 取得單筆使用者記錄。
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    @staticmethod
    def get_by_username(username):
        """
        根據 username 取得單筆使用者記錄。
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有使用者記錄。
        """
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            conn.close()
            return [dict(u) for u in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    @staticmethod
    def update(user_id, password_hash=None, is_admin=None):
        """
        更新指定的 user 記錄。
        只更新傳入且非 None 的參數。
        """
        try:
            conn = get_db_connection()
            user = User.get_by_id(user_id)
            if not user:
                return False
                
            new_password = password_hash if password_hash is not None else user['password_hash']
            new_is_admin = is_admin if is_admin is not None else user['is_admin']
            
            conn.execute(
                'UPDATE users SET password_hash = ?, is_admin = ? WHERE id = ?',
                (new_password, new_is_admin, user_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """
        刪除指定使用者記錄。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
