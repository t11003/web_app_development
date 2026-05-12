from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.database import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    使用者註冊
    輸入：[GET] 無 / [POST] 表單 (username, email, password)
    """
    # 若已登入，導回首頁
    if 'user_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 基礎輸入驗證
        if not username or not email or not password:
            flash('所有欄位皆為必填。', 'danger')
            return render_template('auth/register.html')

        # 檢查信箱是否已存在
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('此信箱已被註冊。', 'danger')
            return render_template('auth/register.html')

        password_hash = generate_password_hash(password)
        try:
            # 建立使用者記錄 (預設角色設為 student)
            User.create(username=username, email=email, password_hash=password_hash, role='student')
            flash('註冊成功！請進行登入。', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('發生未知的錯誤，請稍後再試。', 'danger')

    # GET 請求，渲染註冊表單
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    使用者登入
    輸入：[GET] 無 / [POST] 表單 (email, password)
    """
    # 若已登入，導回首頁
    if 'user_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('請輸入信箱與密碼。', 'warning')
            return render_template('auth/login.html')

        # 查詢使用者並比對密碼
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('信箱或密碼錯誤。', 'danger')

    # GET 請求，渲染登入表單
    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    使用者登出
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))
