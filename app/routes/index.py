from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def dashboard():
    """
    首頁：財務總覽 Dashboard
    HTTP Method: GET
    
    處理邏輯: 
      1. 呼叫 Expense.get_all() 並過濾出「當月」的所有紀錄。
      2. 根據 category_type 統計當月「總收入、總支出」，並算出「當前結餘」。
      3. 準備收支結構圖表所需的圓餅圖資料。
    
    輸出: render_template('index.html', summary=..., chart_data=...)
    錯誤處理: 若當月尚無紀錄，則總計皆回傳 0，前端顯示空白或引導提示。
    """
    pass
