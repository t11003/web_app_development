from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_default_secret')
    
    # 確保 instance 資料夾存在，以供 SQLite 使用
    os.makedirs(app.instance_path, exist_ok=True)
    
    # 註冊 Blueprints
    from app.routes.auth import auth_bp
    from app.routes.recipe import recipe_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipe_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

def init_db():
    from app.models.database import init_db as db_init
    db_init()
