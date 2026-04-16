from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import bcrypt
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單 (templates/auth/register.html)。
    POST: 接收表單資料，驗證輸入是否合法、信箱是否重複，寫入資料庫並重新導向至登入頁面。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 基礎輸入驗證
        if not username or not password or not confirm_password:
            flash('請填寫所有必填欄位！', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('兩次輸入的密碼不一致！', 'danger')
            return redirect(url_for('auth.register'))

        # 檢查帳號是否已被註冊
        existing_user = User.get_by_username(username)
        if existing_user:
            flash('該使用者帳號 (信箱) 已被註冊！', 'danger')
            return redirect(url_for('auth.register'))

        # 密碼雜湊加密 (Bcrypt)
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_id = User.create(username=username, password_hash=password_hash, is_admin=0)
            
            if user_id:
                flash('註冊成功！請登入。', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('系統錯誤，註冊失敗，請稍後再試。', 'danger')
        except Exception as e:
            print(f"Bcrypt Error: {e}")
            flash('伺服器發生例外錯誤。', 'danger')
            
        return redirect(url_for('auth.register'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單 (templates/auth/login.html)。
    POST: 接收表單並比對資料庫密碼，驗證成功後將使用者狀態存入 Session，將用戶導回首頁。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請輸入帳號與密碼！', 'danger')
            return redirect(url_for('auth.login'))

        user = User.get_by_username(username)
        if user:
            # 校驗雜湊密碼
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                # 設定 Session
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = user['is_admin']
                flash('登入成功！', 'success')
                return redirect(url_for('divination.index'))
            
        flash('帳號或密碼錯誤！', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    GET: 清除目前的 Session 登入狀態，重導向至首頁。
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('recipe.index'))
