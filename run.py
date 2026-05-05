import os
from dotenv import load_dotenv
from app import create_app
from app.models.record import init_db

# 載入 .env 環境變數
load_dotenv()

# 建立 Flask 應用程式
app = create_app()

# 設定環境變數中的 SECRET_KEY（若有）
if os.getenv('SECRET_KEY'):
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if __name__ == '__main__':
    # 確保資料庫與資料表已初始化
    init_db()
    # 啟動開發伺服器
    app.run(debug=True)
