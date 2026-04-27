from flask import Blueprint, request, redirect, render_template, flash, url_for
from app.models.transaction import Transaction

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@transaction_bp.route('/', methods=['GET'])
def index():
    """收支查詢清單路由"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        transactions = Transaction.get_by_date_range(start_date, end_date)
    else:
        transactions = Transaction.get_all()
        
    return render_template('transactions/index.html', transactions=transactions, start_date=start_date, end_date=end_date)

@transaction_bp.route('/new', methods=['GET'])
def new_transaction():
    """新增收支表單頁面"""
    tx_type = request.args.get('type', 'EXPENSE')
    return render_template('transactions/form.html', tx_type=tx_type)

@transaction_bp.route('/', methods=['POST'])
def create_transaction():
    """儲存新的收支紀錄"""
    tx_type = request.form.get('type')
    amount_str = request.form.get('amount')
    category = request.form.get('category')
    transaction_date = request.form.get('transaction_date')
    
    if not amount_str or not category or not transaction_date or not tx_type:
        flash('請填寫所有欄位')
        return redirect(url_for('transaction.new_transaction', type=tx_type))
        
    try:
        amount = int(amount_str)
        if amount <= 0:
            raise ValueError()
    except ValueError:
        flash('金額必須為正整數')
        return redirect(url_for('transaction.new_transaction', type=tx_type))
        
    Transaction.create(tx_type, amount, category, transaction_date)
    flash('收支紀錄新增成功')
    return redirect(url_for('main.index'))

@transaction_bp.route('/<int:record_id>/delete', methods=['POST'])
def delete_transaction(record_id):
    """刪除特定收支紀錄"""
    Transaction.delete(record_id)
    flash('紀錄已刪除')
    return redirect(url_for('transaction.index'))
