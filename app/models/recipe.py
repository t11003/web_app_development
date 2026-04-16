from .database import get_db_connection

class Recipe:
    @staticmethod
    def create(user_id, title, steps, is_public=0, cover_image=None):
        """
        新增一筆食譜記錄。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipes (user_id, title, steps, is_public, cover_image) VALUES (?, ?, ?, ?, ?)',
                (user_id, title, steps, is_public, cover_image)
            )
            conn.commit()
            recipe_id = cursor.lastrowid
            conn.close()
            return recipe_id
        except Exception as e:
            print(f"Error creating recipe: {e}")
            return None

    @staticmethod
    def get_by_id(recipe_id):
        """
        取得單筆食譜。
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            conn.close()
            return dict(recipe) if recipe else None
        except Exception as e:
            print(f"Error getting recipe: {e}")
            return None

    @staticmethod
    def get_all_public():
        """
        取得所有公開狀態的食譜。
        """
        try:
            conn = get_db_connection()
            recipes = conn.execute('SELECT * FROM recipes WHERE is_public = 1 ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(r) for r in recipes]
        except Exception as e:
            print(f"Error getting public recipes: {e}")
            return []

    @staticmethod
    def get_by_user_id(user_id):
        """
        依創作者獲取食譜。
        """
        try:
            conn = get_db_connection()
            recipes = conn.execute('SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
            conn.close()
            return [dict(r) for r in recipes]
        except Exception as e:
            print(f"Error getting user recipes: {e}")
            return []
            
    @staticmethod
    def search_by_keyword(keyword, show_private=False, user_id=None):
        """
        關鍵字搜尋食譜。可透過權限參數決定是否能搜尋到私人食譜。
        """
        try:
            conn = get_db_connection()
            query = 'SELECT * FROM recipes WHERE title LIKE ? OR steps LIKE ?'
            params = [f'%{keyword}%', f'%{keyword}%']
            
            if not show_private:
                query += ' AND is_public = 1'
            elif user_id is not None:
                 query += ' AND (is_public = 1 OR user_id = ?)'
                 params.append(user_id)
                 
            query += ' ORDER BY created_at DESC'
            recipes = conn.execute(query, tuple(params)).fetchall()
            conn.close()
            return [dict(r) for r in recipes]
        except Exception as e:
            print(f"Error searching recipes: {e}")
            return []

    @staticmethod
    def update(recipe_id, title=None, steps=None, is_public=None, cover_image=None):
        """
        更新食譜。
        """
        try:
            conn = get_db_connection()
            recipe = Recipe.get_by_id(recipe_id)
            if not recipe:
                return False
                
            new_title = title if title is not None else recipe['title']
            new_steps = steps if steps is not None else recipe['steps']
            new_is_public = is_public if is_public is not None else recipe['is_public']
            new_cover_image = cover_image if cover_image is not None else recipe['cover_image']
            
            conn.execute(
                'UPDATE recipes SET title = ?, steps = ?, is_public = ?, cover_image = ? WHERE id = ?',
                (new_title, new_steps, new_is_public, new_cover_image, recipe_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating recipe: {e}")
            return False

    @staticmethod
    def delete(recipe_id):
        """
        刪除食譜。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting recipe: {e}")
            return False
