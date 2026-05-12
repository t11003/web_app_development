from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.database import Event, Registration
from datetime import datetime

event_bp = Blueprint('event', __name__, url_prefix='/events')

@event_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    # 權限檢查：只有主辦方可以建立活動
    if not session.get('user_id') or session.get('user_role') != 'organizer':
        flash('只有主辦方可以建立活動。', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_date_str = request.form.get('event_date')
        location = request.form.get('location')
        capacity_str = request.form.get('capacity')

        if not all([title, description, event_date_str, location, capacity_str]):
            flash('所有欄位皆為必填。', 'danger')
            return render_template('events/create.html')
            
        try:
            event_date = datetime.fromisoformat(event_date_str)
            capacity = int(capacity_str)
            new_event = Event.create(
                organizer_id=session.get('user_id'),
                title=title,
                description=description,
                event_date=event_date,
                location=location,
                capacity=capacity
            )
            flash('活動建立成功！', 'success')
            return redirect(url_for('event.event_detail', event_id=new_event.id))
        except Exception as e:
            flash(f'建立失敗：{e}', 'danger')

    return render_template('events/create.html')

@event_bp.route('/<int:event_id>', methods=['GET'])
def event_detail(event_id):
    event = Event.get_by_id(event_id)
    if not event:
        flash('找不到該活動。', 'warning')
        return redirect(url_for('main.index'))

    # 計算目前的正取人數
    confirmed_count = sum(1 for r in event.registrations if r.status == 'Confirmed')
    
    # 檢查登入者的報名狀態
    user_reg = None
    if session.get('user_id'):
        for r in event.registrations:
            if r.user_id == session.get('user_id') and r.status != 'Cancelled':
                user_reg = r
                break

    return render_template('events/detail.html', event=event, confirmed_count=confirmed_count, user_reg=user_reg)
