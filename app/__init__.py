import os
from flask import Flask

def create_app():
    """Flask 應用程式工廠函式"""
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = 'dev_secret_key'  # 測試用，實務應從環境變數讀取
    
    # 註冊路由 Blueprint
    from .routes import bp as records_bp
    app.register_blueprint(records_bp)
    
    return app
