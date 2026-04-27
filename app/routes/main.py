from flask import Blueprint, render_template
from app.models.transaction import Transaction
from app.models.fixed_deduction import FixedDeduction
from datetime import datetime

main_bp = Blueprint('main', __name__)

def process_fixed_deductions():
    """背景處理固定扣款邏輯，檢查所有設定，若符合本月且到期則自動扣款"""
    today = datetime.now()
    current_month = today.strftime('%Y-%m')
    current_day = today.day
    
    deductions = FixedDeduction.get_all()
    for d in deductions:
        if d['last_processed_month'] != current_month and d['deduct_day'] <= current_day:
            # 建立支出紀錄
            Transaction.create('EXPENSE', d['amount'], d['category'], today.strftime('%Y-%m-%d'))
            # 更新已處理月份
            FixedDeduction.update_last_processed(d['id'], current_month)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁路由
    """
    # 觸發固定扣款背景處理
    process_fixed_deductions()
    
    # 取得最新資料
    total_balance = Transaction.get_total_balance()
    recent_transactions = Transaction.get_all()[:5]  # 取得最近5筆
    
    return render_template('main/index.html', total_balance=total_balance, transactions=recent_transactions)
