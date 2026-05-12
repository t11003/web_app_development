from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.database import Event, Registration

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/events/<int:event_id>/register', methods=['POST'])
def register_event(event_id):
    if not session.get('user_id'):
        flash('請先登入才能報名。', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    event = Event.get_by_id(event_id)
    if not event:
        flash('找不到該活動。', 'danger')
        return redirect(url_for('main.index'))

    # 檢查是否已報名
    existing_reg = Registration.query.filter_by(event_id=event_id, user_id=user_id).filter(Registration.status != 'Cancelled').first()
    if existing_reg:
        flash('您已經報名或候補此活動了。', 'info')
        return redirect(url_for('event.event_detail', event_id=event_id))

    # 計算目前的正取人數
    confirmed_count = Registration.query.filter_by(event_id=event_id, status='Confirmed').count()
    
    if confirmed_count < event.capacity:
        status = 'Confirmed'
        msg = '報名成功！您已正取。'
    else:
        status = 'Waitlist'
        msg = '名額已滿，您已自動轉入候補名單。'

    try:
        Registration.create(event_id=event_id, user_id=user_id, status=status)
        flash(msg, 'success')
    except Exception as e:
        flash(f'報名失敗：{e}', 'danger')

    return redirect(url_for('registration.my_registrations'))

@registration_bp.route('/events/<int:event_id>/cancel', methods=['POST'])
def cancel_registration(event_id):
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    reg = Registration.query.filter_by(event_id=event_id, user_id=user_id).filter(Registration.status != 'Cancelled').first()
    
    if not reg:
        flash('找不到您的報名紀錄。', 'danger')
        return redirect(url_for('event.event_detail', event_id=event_id))

    try:
        was_confirmed = (reg.status == 'Confirmed')
        reg.update_status('Cancelled')
        flash('已取消報名。', 'success')

        # 如果取消的是正取，且有候補名單，則自動遞補第一順位
        if was_confirmed:
            next_waitlist = Registration.query.filter_by(event_id=event_id, status='Waitlist').order_by(Registration.created_at.asc()).first()
            if next_waitlist:
                next_waitlist.update_status('Confirmed')

    except Exception as e:
        flash(f'取消失敗：{e}', 'danger')

    return redirect(url_for('event.event_detail', event_id=event_id))

@registration_bp.route('/my_registrations', methods=['GET'])
def my_registrations():
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    regs = Registration.get_user_registrations(user_id)
    return render_template('registrations/my_list.html', registrations=regs)
