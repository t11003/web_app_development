import os
from flask import Flask
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='app/templates')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
    
    # 載入並註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.transaction import transaction_bp
    from app.routes.fixed_deduction import fixed_deduction_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(fixed_deduction_bp)
    
    # 初始化資料庫
    from app.models.db import init_db
    init_db()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
