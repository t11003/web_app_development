from flask import Flask
from app.routes.recipe import recipe_bp

def create_app():
    # 指定 template 與 static 的存放路徑，確保與專案結構相符
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 註冊 Blueprints
    app.register_blueprint(recipe_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
