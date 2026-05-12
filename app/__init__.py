from flask import Flask
import os
from .models.database import db

# 載入路由 Blueprints
from .routes.main_routes import main_bp
from .routes.auth_routes import auth_bp
from .routes.event_routes import event_bp
from .routes.registration_routes import registration_bp

def create_app(test_config=None):
    # 建立與設定 app
    app = Flask(__name__, instance_relative_config=True)
    
    # 確保 sqlite 在 Windows 的絕對路徑不會因 \ 造成 500 錯誤
    db_path = os.path.join(app.instance_path, 'application.db')
    sqlite_uri = 'sqlite:///' + db_path.replace('\\', '/')
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=sqlite_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # 如果有 instance/config.py，則載入
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 使用測試設定
        app.config.from_mapping(test_config)

    # 確保 instance_path 存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫
    db.init_app(app)

    # 註冊 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(registration_bp)

    return app
