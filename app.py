import os
from dotenv import load_dotenv
from app import create_app
from app.models.database import db

# 載入環境變數
load_dotenv()

app = create_app()

# 初始化建立資料表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
