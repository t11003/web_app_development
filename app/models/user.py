from .database import get_db_connection

class User:
    @staticmethod
    def create(username, password_hash, is_admin=0):
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

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def update(user_id, password_hash=None, is_admin=None):
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

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
