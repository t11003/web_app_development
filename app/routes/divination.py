from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import random
from app.models.divination import Divination

divination_bp = Blueprint('divination', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入以使用專屬占卜與完整紀錄功能！', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@divination_bp.route('/', methods=['GET'])
def index():
    return render_template('divination/index.html')

@divination_bp.route('/divination/temple', methods=['GET', 'POST'])
@login_required
def temple_draw():
    if request.method == 'POST':
        question = request.form.get('question', '未填寫問題')
        
        # Simulate simple 60-jiazi draw
        draw_number = random.randint(1, 60)
        result_title = f"觀音靈籤 第 {draw_number} 籤"
        explanation = f"針對您的問題：「{question}」。\n這支籤代表著順流而行，切莫急躁。萬事互相效力，時間到了自然會有好的結果展開。建議您保持內心的平靜，多做善事累積福報。神明指示您只需依循本心，凡事不強求。"
        
        div_id = Divination.create(session['user_id'], 'temple', question, result_title, explanation)
        if div_id:
            flash('求籤成功！神明已經給予了指引。', 'success')
            return redirect(url_for('divination.result', id=div_id))
        else:
            flash('系統發生錯誤，無法儲存。', 'danger')
            
    return render_template('divination/temple_draw.html')

@divination_bp.route('/divination/tarot', methods=['GET', 'POST'])
@login_required
def tarot_draw():
    if request.method == 'POST':
        question = request.form.get('question', '未填寫問題')
        
        # Simple Major Arcana simulate
        tarot_cards = ["愚者 (The Fool)", "魔術師 (The Magician)", "女祭司 (The High Priestess)", "皇后 (The Empress)", "皇帝 (The Emperor)", "教皇 (The Hierophant)", "戀人 (The Lovers)", "戰車 (The Chariot)", "力量 (Strength)", "隱者 (The Hermit)", "命運之輪 (Wheel of Fortune)", "正義 (Justice)", "太陽 (The Sun)", "世界 (The World)"]
        card = random.choice(tarot_cards)
        position = random.choice(["正位", "逆位"])
        result_title = f"{card} - {position}"
        
        explanation = f"針對您的問題：「{question}」。\n您抽到了充滿靈性的代表牌。這象徵著您正面臨一個關鍵的轉折點，傾聽自己內心的聲音將是最佳解答。宇宙正在暗中協助您度過難關，請保持正能量。"
        
        div_id = Divination.create(session['user_id'], 'tarot', question, result_title, explanation)
        if div_id:
            flash('塔羅抽牌完成！宇宙傳遞了深層的訊息。', 'success')
            return redirect(url_for('divination.result', id=div_id))
        else:
            flash('系統發生錯誤，無法儲存。', 'danger')
            
    return render_template('divination/tarot_draw.html')

@divination_bp.route('/divination/result/<int:id>', methods=['GET'])
@login_required
def result(id):
    div = Divination.get_by_id(id)
    if not div or div['user_id'] != session['user_id']:
        flash('找不到該紀錄或您沒有權限。', 'danger')
        return redirect(url_for('divination.index'))
    return render_template('divination/result.html', div=div)

@divination_bp.route('/divination/history', methods=['GET'])
@login_required
def history():
    divs = Divination.get_by_user_id(session['user_id'])
    return render_template('divination/history.html', divs=divs)

@divination_bp.route('/divination/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    div = Divination.get_by_id(id)
    if div and div['user_id'] == session['user_id']:
        Divination.delete(id)
        flash('紀錄已成功刪除。', 'info')
    return redirect(url_for('divination.history'))
