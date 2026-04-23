from flask import Blueprint, render_template, request, redirect, url_for, flash

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/')
def list_categories():
    """
    分類列表
    HTTP Method: GET
    處理邏輯: 呼叫 Category.get_all() 取得所有分類資料
    輸出: render_template('categories/index.html', categories=categories)
    """
    pass

@category_bp.route('/new', methods=['GET', 'POST'])
def new_category():
    """
    新增分類
    HTTP Method: GET, POST
    
    [GET]
      處理邏輯: 單純回傳新增表單的介面
      輸出: render_template('categories/form.html')
      
    [POST]
      輸入: request.form (包含 name, type)
      處理邏輯: 檢查名稱不為空，呼叫 Category.create(name, type, is_preset=0)
      輸出: redirect(url_for('category.list_categories'))
      錯誤處理: 名稱為空或類型不合法時，使用 flash() 紀錄錯誤，並回傳原表單頁面 
    """
    pass

@category_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_category(id):
    """
    編輯自訂分類
    HTTP Method: GET, POST
    
    [GET]
      處理邏輯: 
        1. Category.get_by_id(id) 若找不到回傳 404。
        2. 檢查 is_preset == 1，若是預設分類則 flash 錯誤並拒絕編輯。
      輸出: render_template('categories/form.html', category=category)
      
    [POST]
      輸入: request.form (包含 name)
      處理邏輯: Category.update(id, name) [僅允許更改名稱]
      輸出: redirect(url_for('category.list_categories'))
    """
    pass

@category_bp.route('/<int:id>/delete', methods=['POST'])
def delete_category(id):
    """
    刪除自訂分類
    HTTP Method: POST
    
    處理邏輯:
      1. Category.get_by_id(id)，檢查是否為預設分類，若是則拒絕。
      2. (Nice to Have) 檢查是否有 expenses 依賴該分類，若有則閃爍錯誤提示不允許刪除。
      3. Category.delete(id)
    輸出: redirect(url_for('category.list_categories'))
    """
    pass
