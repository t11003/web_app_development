import sqlite3
from app.models.db import get_db_connection

class FixedDeduction:
    @staticmethod
    def create(amount, category, deduct_day):
        """
        新增一筆記錄
        :param amount: 扣款金額
        :param category: 扣款分類
        :param deduct_day: 每月固定扣款日 (1-31)
        :return: 新增成功的紀錄 ID，若失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO fixed_deductions (amount, category, deduct_day) VALUES (?, ?, ?)",
                    (amount, category, deduct_day)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in FixedDeduction.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有記錄
        :return: 紀錄列表 (sqlite3.Row 格式)
        """
        try:
            with get_db_connection() as conn:
                return conn.execute("SELECT * FROM fixed_deductions ORDER BY deduct_day ASC").fetchall()
        except sqlite3.Error as e:
            print(f"Database error in FixedDeduction.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(deduction_id):
        """
        取得單筆記錄
        :param deduction_id: FixedDeduction ID
        :return: 該筆記錄 (sqlite3.Row) 或 None
        """
        try:
            with get_db_connection() as conn:
                return conn.execute("SELECT * FROM fixed_deductions WHERE id = ?", (deduction_id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Database error in FixedDeduction.get_by_id: {e}")
            return None

    @staticmethod
    def update(deduction_id, amount, category, deduct_day):
        """
        更新記錄
        :param deduction_id: FixedDeduction ID
        :return: 成功與否的布林值
        """
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "UPDATE fixed_deductions SET amount=?, category=?, deduct_day=? WHERE id=?",
                    (amount, category, deduct_day, deduction_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in FixedDeduction.update: {e}")
            return False

    @staticmethod
    def update_last_processed(deduction_id, processed_month):
        """
        更新記錄最後被處理的月份
        :param deduction_id: FixedDeduction ID
        :param processed_month: 處理的月份字串 (YYYY-MM)
        :return: 成功與否的布林值
        """
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "UPDATE fixed_deductions SET last_processed_month = ? WHERE id = ?",
                    (processed_month, deduction_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in FixedDeduction.update_last_processed: {e}")
            return False

    @staticmethod
    def delete(deduction_id):
        """
        刪除記錄
        :param deduction_id: FixedDeduction ID
        :return: 成功與否的布林值
        """
        try:
            with get_db_connection() as conn:
                conn.execute("DELETE FROM fixed_deductions WHERE id = ?", (deduction_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in FixedDeduction.delete: {e}")
            return False
