from flask import Blueprint, render_template, request
from app.models.database import Event

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁 / 活動列表
    輸入：無 (可接受 keyword 參數)
    處理邏輯：呼叫 Event.get_all(keyword) 取出所有活動，按時間排序
    輸出：渲染 templates/index.html
    """
    keyword = request.args.get('keyword', '').strip()
    events = Event.get_all(keyword=keyword)
    return render_template('index.html', events=events, keyword=keyword)
