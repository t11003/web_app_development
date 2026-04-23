from flask import Blueprint, render_template, request, redirect, url_for, flash

expense_bp = Blueprint('expense', __name__, url_prefix='/expenses')

@expense_bp.route('/')
def list_expenses():
    """
    列出所有收支明細
    HTTP Method: GET
    
    輸入: (可選) Query String 提供月份過濾，例如 ?month=2024-03
    處理邏輯: 呼叫 Expense.get_all() 載入所有紀錄
    輸出: render_template('expenses/index.html', expenses=expenses)
    """
    pass

@expense_bp.route('/new', methods=['GET', 'POST'])
def new_expense():
    """
    新增收支紀錄
    HTTP Method: GET, POST
    
    [GET] 
      處理邏輯: 呼叫 Category.get_all() 將分類選項餵給前端的下拉選單
      輸出: render_template('expenses/form.html', categories=categories)
      
    [POST]
      輸入: request.form (包含 amount, category_id, date, note)
      處理邏輯: 確保金額為正數、必填欄位不為空，接著呼叫 Expense.create()
      輸出: 新增成功後 redirect(url_for('expense.list_expenses'))
      錯誤處理: 資料缺失或格式錯誤時，使用 flash() 紀錄錯誤並重導回表單頁面
    """
    pass

@expense_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_expense(id):
    """
    編輯收支紀錄
    HTTP Method: GET, POST
    
    [GET] 
      處理邏輯: 
        1. Expense.get_by_id(id) 取得該筆紀錄內容，如果不存在則丟出 404。
        2. 取 Category.get_all() 餵給前端的下拉選單。
      輸出: render_template('expenses/form.html', expense=expense, categories=categories)
      
    [POST]
      輸入: request.form (包含 amount, category_id, date, note)
      處理邏輯: 基礎邏輯檢查，執行 Expense.update()
      輸出: redirect(url_for('expense.list_expenses'))
    """
    pass

@expense_bp.route('/<int:id>/delete', methods=['POST'])
def delete_expense(id):
    """
    刪除收支紀錄
    HTTP Method: POST
    
    處理邏輯: 呼叫 Expense.delete(id)
    輸出: redirect(url_for('expense.list_expenses'))
    錯誤處理: 找不到對應 ID 紀錄時可回傳 404 或 flash()
    """
    pass
