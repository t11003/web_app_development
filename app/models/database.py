from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    使用者模型：代表學生或主辦方
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    events_organized = db.relationship('Event', backref='organizer', lazy=True)
    registrations = db.relationship('Registration', backref='user', lazy=True)

    @classmethod
    def create(cls, username, email, password_hash, role='student'):
        """
        新增一筆使用者記錄
        """
        try:
            new_user = cls(username=username, email=email, password_hash=password_hash, role=role)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            raise

    @classmethod
    def get_by_id(cls, user_id):
        """
        取得單筆使用者記錄
        """
        try:
            return cls.query.get(user_id)
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None


class Event(db.Model):
    """
    活動模型：代表主辦方建立的活動
    """
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    registrations = db.relationship('Registration', backref='event', lazy=True)

    @classmethod
    def create(cls, organizer_id, title, description, event_date, location, capacity):
        """
        新增一筆活動記錄
        """
        try:
            new_event = cls(
                organizer_id=organizer_id, 
                title=title, 
                description=description, 
                event_date=event_date, 
                location=location, 
                capacity=capacity
            )
            db.session.add(new_event)
            db.session.commit()
            return new_event
        except Exception as e:
            db.session.rollback()
            print(f"Error creating event: {e}")
            raise

    @classmethod
    def get_all(cls, keyword=None):
        """
        取得所有活動記錄，依建立時間遞減排序，支援關鍵字搜尋
        """
        try:
            query = cls.query
            if keyword:
                search_term = f"%{keyword}%"
                query = query.filter(db.or_(cls.title.ilike(search_term), cls.description.ilike(search_term)))
            return query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting all events: {e}")
            return []

    @classmethod
    def get_by_id(cls, event_id):
        """
        取得單筆活動記錄
        """
        try:
            return cls.query.get(event_id)
        except Exception as e:
            print(f"Error getting event by id: {e}")
            return None

    def update(self, **kwargs):
        """
        更新活動記錄
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating event: {e}")
            raise

    def delete(self):
        """
        刪除活動記錄
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting event: {e}")
            raise


class Registration(db.Model):
    """
    報名記錄模型：追蹤學生報名狀態
    """
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False) # 'Confirmed', 'Waitlist', 'Cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, event_id, user_id, status):
        """
        新增一筆報名記錄
        """
        try:
            new_reg = cls(event_id=event_id, user_id=user_id, status=status)
            db.session.add(new_reg)
            db.session.commit()
            return new_reg
        except Exception as e:
            db.session.rollback()
            print(f"Error creating registration: {e}")
            raise

    @classmethod
    def get_by_id(cls, reg_id):
        """
        取得單筆報名記錄
        """
        try:
            return cls.query.get(reg_id)
        except Exception as e:
            print(f"Error getting registration by id: {e}")
            return None

    @classmethod
    def get_user_registrations(cls, user_id):
        """
        取得指定使用者的所有報名記錄
        """
        try:
            return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting user registrations: {e}")
            return []

    def update_status(self, new_status):
        """
        更新報名記錄狀態
        """
        try:
            self.status = new_status
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating registration status: {e}")
            raise
