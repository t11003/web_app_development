import sqlite3
from app.models.db import get_db_connection

class Transaction:
    @staticmethod
    def create(tx_type, amount, category, transaction_date):
        """
        新增一筆記錄
        :param tx_type: 'INCOME' 或 'EXPENSE'
        :param amount: 金額
        :param category: 分類
        :param transaction_date: 交易日期 (YYYY-MM-DD)
        :return: 新增成功的紀錄 ID，若失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO transactions (type, amount, category, transaction_date) VALUES (?, ?, ?, ?)",
                    (tx_type, amount, category, transaction_date)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in Transaction.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有記錄
        :return: 紀錄列表 (sqlite3.Row 格式)
        """
        try:
            with get_db_connection() as conn:
                return conn.execute(
                    "SELECT * FROM transactions ORDER BY transaction_date DESC, created_at DESC"
                ).fetchall()
        except sqlite3.Error as e:
            print(f"Database error in Transaction.get_all: {e}")
            return []

    @staticmethod
    def get_by_date_range(start_date, end_date):
        """
        取得指定日期區間的紀錄
        :return: 紀錄列表
        """
        try:
            with get_db_connection() as conn:
                return conn.execute(
                    "SELECT * FROM transactions WHERE transaction_date >= ? AND transaction_date <= ? ORDER BY transaction_date DESC, created_at DESC",
                    (start_date, end_date)
                ).fetchall()
        except sqlite3.Error as e:
            print(f"Database error in Transaction.get_by_date_range: {e}")
            return []

    @staticmethod
    def get_by_id(tx_id):
        """
        取得單筆記錄
        :param tx_id: Transaction ID
        :return: 該筆記錄 (sqlite3.Row) 或 None
        """
        try:
            with get_db_connection() as conn:
                return conn.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Database error in Transaction.get_by_id: {e}")
            return None

    @staticmethod
    def update(tx_id, tx_type, amount, category, transaction_date):
        """
        更新記錄
        :param tx_id: Transaction ID
        :return: 成功與否的布林值
        """
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "UPDATE transactions SET type=?, amount=?, category=?, transaction_date=? WHERE id=?",
                    (tx_type, amount, category, transaction_date, tx_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in Transaction.update: {e}")
            return False

    @staticmethod
    def delete(tx_id):
        """
        刪除記錄
        :param tx_id: Transaction ID
        :return: 成功與否的布林值
        """
        try:
            with get_db_connection() as conn:
                conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in Transaction.delete: {e}")
            return False

    @staticmethod
    def get_total_balance():
        """
        取得當前總餘額
        :return: 總餘額數值
        """
        try:
            with get_db_connection() as conn:
                # 簡化計算方式，取收入總和與支出總和
                result = conn.execute("""
                    SELECT 
                        SUM(CASE WHEN type='INCOME' THEN amount ELSE 0 END) as total_income,
                        SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) as total_expense
                    FROM transactions
                """).fetchone()
                
                income = result['total_income'] if result['total_income'] else 0
                expense = result['total_expense'] if result['total_expense'] else 0
                return income - expense
        except sqlite3.Error as e:
            print(f"Database error in Transaction.get_total_balance: {e}")
            return 0
