from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.donation import Donation

donation_bp = Blueprint('donation', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入會員以完成線上隨喜程序。', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@donation_bp.route('/', methods=['GET'])
def donate():
    return render_template('donation/donate.html')

@donation_bp.route('/process', methods=['POST'])
@login_required
def process():
    amount = request.form.get('amount', type=int, default=0)
    if amount <= 0:
        flash('請輸入大於0的金額。', 'danger')
        return redirect(url_for('donation.donate'))
        
    # Simulate payment processing MVP
    don_id = Donation.create(session['user_id'], amount, status='completed')
    if don_id:
        return redirect(url_for('donation.thanks', amount=amount))
    else:
        flash('處理發生錯誤。', 'danger')
        return redirect(url_for('donation.donate'))

@donation_bp.route('/thanks', methods=['GET'])
@login_required
def thanks():
    amount = request.args.get('amount', 0)
    return render_template('donation/thanks.html', amount=amount)
