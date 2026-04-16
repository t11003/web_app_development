from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
def index():
    if not session.get('user_id') or not session.get('is_admin'):
        flash('您未具備管理員權限！', 'danger')
        return redirect(url_for('recipe.index'))
    users = User.get_all()
    recipes = Recipe.search_by_keyword('', show_private=True, user_id=None)
    return render_template('admin/dashboard.html', users=users, recipes=recipes)

@admin_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    if not session.get('user_id') or not session.get('is_admin'):
        flash('您未具備管理員權限！', 'danger')
        return redirect(url_for('recipe.index'))
    Ingredient.clear_recipe_ingredients(id)
    Recipe.delete(id)
    flash('已強制刪除違規資料。', 'success')
    return redirect(url_for('admin.index'))