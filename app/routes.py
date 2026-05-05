from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.record import RecordModel

# 建立一個 Blueprint 來管理收支紀錄相關路由
bp = Blueprint('records', __name__)

@bp.route('/')
def index():
    """
    [GET] 首頁
    顯示目前總餘額以及近期的收支歷史紀錄
    """
    balance = RecordModel.get_balance()
    records = RecordModel.get_all()
    return render_template('index.html', balance=balance, records=records)

@bp.route('/records/new', methods=['GET'])
def new_record():
    """
    [GET] 新增紀錄頁面
    顯示填寫收支資料的表單
    """
    return render_template('records/new.html')

@bp.route('/records', methods=['POST'])
def create_record():
    """
    [POST] 送出新增紀錄
    接收表單資料並寫入資料庫，完成後導回首頁
    """
    record_type = request.form.get('type')
    amount = request.form.get('amount')
    date = request.form.get('date')
    category = request.form.get('category', '')
    description = request.form.get('description', '')

    # 基本輸入驗證
    if not record_type or not amount or not date:
        flash('收支類型、金額與日期為必填欄位！', 'danger')
        return redirect(url_for('records.new_record'))

    try:
        amount = int(amount)
    except ValueError:
        flash('金額必須為有效的數字！', 'danger')
        return redirect(url_for('records.new_record'))

    # 寫入資料庫
    new_id = RecordModel.create(record_type, amount, date, category, description)
    if new_id:
        flash('新增紀錄成功！', 'success')
    else:
        flash('新增失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('records.index'))

@bp.route('/records/<int:record_id>/edit', methods=['GET'])
def edit_record(record_id):
    """
    [GET] 編輯紀錄頁面
    顯示帶有原始資料的編輯表單頁面
    """
    record = RecordModel.get_by_id(record_id)
    if not record:
        abort(404)
        
    return render_template('records/edit.html', record=record)

@bp.route('/records/<int:record_id>/update', methods=['POST'])
def update_record(record_id):
    """
    [POST] 更新紀錄
    接收更新資料並寫入資料庫，完成後導回首頁
    """
    # 檢查該筆資料是否存在
    record = RecordModel.get_by_id(record_id)
    if not record:
        abort(404)

    record_type = request.form.get('type')
    amount = request.form.get('amount')
    date = request.form.get('date')
    category = request.form.get('category', '')
    description = request.form.get('description', '')

    if not record_type or not amount or not date:
        flash('收支類型、金額與日期為必填欄位！', 'danger')
        return redirect(url_for('records.edit_record', record_id=record_id))

    try:
        amount = int(amount)
    except ValueError:
        flash('金額必須為有效的數字！', 'danger')
        return redirect(url_for('records.edit_record', record_id=record_id))

    success = RecordModel.update(record_id, record_type, amount, date, category, description)
    if success:
        flash('更新紀錄成功！', 'success')
    else:
        flash('更新失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('records.index'))

@bp.route('/records/<int:record_id>/delete', methods=['POST'])
def delete_record(record_id):
    """
    [POST] 刪除紀錄
    將指定 ID 的收支紀錄從資料庫中刪除，並導回首頁
    """
    success = RecordModel.delete(record_id)
    if success:
        flash('已成功刪除紀錄！', 'success')
    else:
        flash('刪除失敗，找不到該筆紀錄或發生錯誤。', 'danger')
        
    return redirect(url_for('records.index'))
