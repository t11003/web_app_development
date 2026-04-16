from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.user import User

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
def index():
    recipes = Recipe.get_all_public()
    return render_template('recipe/index.html', recipes=recipes)

@recipe_bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    recipes = Recipe.search_by_keyword(q)
    return render_template('recipe/search_results.html', recipes=recipes, keyword=q)

@recipe_bp.route('/search/ingredients', methods=['GET'])
def ingredient_search():
    items_str = request.args.get('items', '')
    if items_str.strip():
        items = [i.strip() for i in items_str.split(',') if i.strip()]
        recipes = Ingredient.search_recipes_by_ingredients(items)
    else:
        items = []
        recipes = []
    return render_template('recipe/ingredient_search.html', recipes=recipes, items=items)

@recipe_bp.route('/recipe/<int:id>', methods=['GET'])
def detail(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('食譜不存在', 'danger')
        return redirect(url_for('recipe.index'))
    if not recipe['is_public']:
        if session.get('user_id') != recipe['user_id'] and not session.get('is_admin'):
            flash('您沒有權限檢視此食譜', 'danger')
            return redirect(url_for('recipe.index'))
    ingredients = Ingredient.get_ingredients_for_recipe(id)
    author = User.get_by_id(recipe['user_id'])
    return render_template('recipe/detail.html', recipe=recipe, ingredients=ingredients, author=author)

@recipe_bp.route('/recipe/my', methods=['GET'])
def my_recipes():
    if not session.get('user_id'):
        flash('請先登入', 'danger')
        return redirect(url_for('auth.login'))
    recipes = Recipe.get_by_user_id(session['user_id'])
    return render_template('recipe/my_recipes.html', recipes=recipes)

@recipe_bp.route('/recipe/new', methods=['GET', 'POST'])
def new_recipe():
    if not session.get('user_id'):
        flash('請先登入', 'danger')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        title = request.form.get('title')
        steps = request.form.get('steps')
        is_public = 1 if request.form.get('is_public') else 0
        ingredients_input = request.form.get('ingredients')
        if not title or not steps:
            flash('標題與步驟為必填', 'danger')
            return redirect(url_for('recipe.new_recipe'))
        recipe_id = Recipe.create(session['user_id'], title, steps, is_public, None)
        if ingredients_input:
            items = [i.strip() for i in ingredients_input.split(',')]
            for item in items:
                if item:
                    ing_id = Ingredient.create(item)
                    Ingredient.link_recipe_ingredient(recipe_id, ing_id)
        flash('建立成功！', 'success')
        return redirect(url_for('recipe.detail', id=recipe_id))
    return render_template('recipe/new.html')

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    if not session.get('user_id'):
        flash('請先登入', 'danger')
        return redirect(url_for('auth.login'))
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('權限不足', 'danger')
        return redirect(url_for('recipe.index'))
    if request.method == 'POST':
        title = request.form.get('title')
        steps = request.form.get('steps')
        is_public = 1 if request.form.get('is_public') else 0
        ingredients_input = request.form.get('ingredients')
        Recipe.update(id, title=title, steps=steps, is_public=is_public)
        Ingredient.clear_recipe_ingredients(id)
        if ingredients_input:
            items = [i.strip() for i in ingredients_input.split(',')]
            for item in items:
                if item:
                    ing_id = Ingredient.create(item)
                    Ingredient.link_recipe_ingredient(id, ing_id)
        flash('更新成功！', 'success')
        return redirect(url_for('recipe.detail', id=id))
    current_ingredients = Ingredient.get_ingredients_for_recipe(id)
    ing_str = ", ".join([i['name'] for i in current_ingredients])
    return render_template('recipe/edit.html', recipe=recipe, ingredients=ing_str)

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    if not session.get('user_id'):
        flash('請先登入', 'danger')
        return redirect(url_for('auth.login'))
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('權限不足', 'danger')
        return redirect(url_for('recipe.index'))
    Ingredient.clear_recipe_ingredients(id)
    Recipe.delete(id)
    flash('刪除成功', 'success')
    return redirect(url_for('recipe.my_recipes'))