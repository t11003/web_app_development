from .database import get_db_connection

class Ingredient:
    @staticmethod
    def create(name):
        """
        新增單一食材，若已存在則取得它的 ID 回傳。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO ingredients (name) VALUES (?)', (name,))
                conn.commit()
                ingredient_id = cursor.lastrowid
            except conn.IntegrityError:
                ingredient = cursor.execute('SELECT id FROM ingredients WHERE name = ?', (name,)).fetchone()
                ingredient_id = ingredient['id']
            conn.close()
            return ingredient_id
        except Exception as e:
            print(f"Error creating ingredient: {e}")
            return None

    @staticmethod
    def get_by_id(ingredient_id):
        """取得單筆食材"""
        try:
            conn = get_db_connection()
            ingredient = conn.execute('SELECT * FROM ingredients WHERE id = ?', (ingredient_id,)).fetchone()
            conn.close()
            return dict(ingredient) if ingredient else None
        except Exception as e:
            print(f"Error getting ingredient: {e}")
            return None

    @staticmethod
    def get_by_name(name):
        """用名稱取得食材"""
        try:
            conn = get_db_connection()
            ingredient = conn.execute('SELECT * FROM ingredients WHERE name = ?', (name,)).fetchone()
            conn.close()
            return dict(ingredient) if ingredient else None
        except Exception as e:
            print(f"Error getting ingredient: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有食材"""
        try:
            conn = get_db_connection()
            ingredients = conn.execute('SELECT * FROM ingredients ORDER BY name').fetchall()
            conn.close()
            return [dict(i) for i in ingredients]
        except Exception as e:
            print(f"Error getting all ingredients: {e}")
            return []

    @staticmethod
    def link_recipe_ingredient(recipe_id, ingredient_id):
        """將食譜與食材綁定（建立多對多關係資料）"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipe_ingredient_map (recipe_id, ingredient_id) VALUES (?, ?)',
                (recipe_id, ingredient_id)
            )
            conn.commit()
            map_id = cursor.lastrowid
            conn.close()
            return map_id
        except Exception as e:
            print(f"Error linking recipe and ingredient: {e}")
            return None
            
    @staticmethod
    def clear_recipe_ingredients(recipe_id):
        """清空一份食譜下的所有食材關聯"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM recipe_ingredient_map WHERE recipe_id = ?', (recipe_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing recipe ingredients: {e}")
            return False

    @staticmethod
    def get_ingredients_for_recipe(recipe_id):
        """傳入食譜 ID，取得它所包含的所有食材陣列"""
        try:
            conn = get_db_connection()
            query = '''
                SELECT i.* FROM ingredients i
                JOIN recipe_ingredient_map m ON i.id = m.ingredient_id
                WHERE m.recipe_id = ?
            '''
            ingredients = conn.execute(query, (recipe_id,)).fetchall()
            conn.close()
            return [dict(i) for i in ingredients]
        except Exception as e:
            print(f"Error getting ingredients for recipe: {e}")
            return []

    @staticmethod
    def search_recipes_by_ingredients(ingredient_names, show_private=False, user_id=None):
        """根據傳入的多組食材陣列名稱，找出完全滿足擁有的食譜清單"""
        if not ingredient_names:
            return []
            
        try:
            conn = get_db_connection()
            placeholders = ', '.join(['?'] * len(ingredient_names))
            
            query = f'''
                SELECT r.* FROM recipes r
                JOIN recipe_ingredient_map m ON r.id = m.recipe_id
                JOIN ingredients i ON m.ingredient_id = i.id
                WHERE i.name IN ({placeholders})
            '''
            
            if not show_private:
                query += ' AND r.is_public = 1'
            elif user_id is not None:
                 query += ' AND (r.is_public = 1 OR r.user_id = ?)'
                 
            query += ' GROUP BY r.id HAVING COUNT(DISTINCT i.id) >= ? ORDER BY r.created_at DESC'
            
            params = list(ingredient_names)
            if user_id is not None and show_private:
                 params.append(user_id)
            params.append(len(ingredient_names))
                 
            recipes = conn.execute(query, tuple(params)).fetchall()
            conn.close()
            return [dict(r) for r in recipes]
        except Exception as e:
            print(f"Error searching recipes by ingredients: {e}")
            return []
