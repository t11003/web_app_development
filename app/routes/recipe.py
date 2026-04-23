from flask import Blueprint, request, render_template, redirect, url_for, abort

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    列出所有食譜。
    若有 ?q= 參數則篩選標題與食材。
    """
    pass

@recipe_bp.route('/recipes/new')
def new_recipe():
    """
    顯示新增食譜表單頁面。
    """
    pass

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    處理新增食譜請求。
    接收表單資料，寫入 DB，完成後導回首頁。
    """
    pass

@recipe_bp.route('/recipes/<int:id>')
def show_recipe(id):
    """
    顯示單一食譜的詳細資料。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    """
    顯示修改食譜的表單頁面，將原資料填入表單中。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    處裡食譜修改請求並寫入。
    更新後導回食譜明細頁。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除指定食譜。
    刪除後導向回首頁。
    """
    pass
