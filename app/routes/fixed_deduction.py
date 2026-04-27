from flask import Blueprint, request, redirect, render_template, flash, url_for
from app.models.fixed_deduction import FixedDeduction

fixed_deduction_bp = Blueprint('fixed_deduction', __name__, url_prefix='/fixed-deductions')

@fixed_deduction_bp.route('/', methods=['GET'])
def index():
    """檢視所有的每月固定扣款清單"""
    deductions = FixedDeduction.get_all()
    return render_template('fixed_deductions/index.html', deductions=deductions)

@fixed_deduction_bp.route('/new', methods=['GET'])
def new_fixed_deduction():
    """顯示新增固定扣款的表單介面"""
    return render_template('fixed_deductions/form.html')

@fixed_deduction_bp.route('/', methods=['POST'])
def create_fixed_deduction():
    """寫入新的固定扣款設定"""
    amount_str = request.form.get('amount')
    category = request.form.get('category')
    deduct_day_str = request.form.get('deduct_day')
    
    if not amount_str or not category or not deduct_day_str:
        flash('請填寫所有欄位')
        return redirect(url_for('fixed_deduction.new_fixed_deduction'))
        
    try:
        amount = int(amount_str)
        deduct_day = int(deduct_day_str)
        if amount <= 0:
            flash('金額必須為正整數')
            return redirect(url_for('fixed_deduction.new_fixed_deduction'))
        if deduct_day < 1 or deduct_day > 31:
            flash('扣款日必須在 1 到 31 之間')
            return redirect(url_for('fixed_deduction.new_fixed_deduction'))
    except ValueError:
        flash('金額與日期必須為正整數')
        return redirect(url_for('fixed_deduction.new_fixed_deduction'))
        
    FixedDeduction.create(amount, category, deduct_day)
    flash('固定扣款設定新增成功')
    return redirect(url_for('fixed_deduction.index'))

@fixed_deduction_bp.route('/<int:deduction_id>/delete', methods=['POST'])
def delete_fixed_deduction(deduction_id):
    """刪除指定的每月固定扣款"""
    FixedDeduction.delete(deduction_id)
    flash('固定扣款已刪除')
    return redirect(url_for('fixed_deduction.index'))
