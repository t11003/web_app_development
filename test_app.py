import os
from app import create_app
from app.models.database import init_db
import sys

# Remove old db if exists to start fresh
if os.path.exists('instance/database.db'):
    os.remove('instance/database.db')

init_db()
app = create_app()
app.testing = True
client = app.test_client()

print("[1] Testing Index (GET /)...")
res = client.get('/', follow_redirects=True)
assert res.status_code == 200, "Index failed"
print("OK Index works.")

print("[2] Testing User Registration (POST /auth/register)...")
res = client.post('/auth/register', data={
    'username':'test_chef_1', 
    'password':'mypassword', 
    'confirm_password':'mypassword'
}, follow_redirects=True)
assert res.status_code == 200
print("OK Registration works.")

print("[3] Testing User Login (POST /auth/login)...")
res = client.post('/auth/login', data={
    'username':'test_chef_1', 
    'password':'mypassword'
}, follow_redirects=True)
assert res.status_code == 200
assert b'test_chef_1' in res.data, "Login failed to set session / show username."
print("OK Login works.")

print("[4] Testing Recipe Creation (POST /recipe/new)...")
res = client.post('/recipe/new', data={
    'title': 'Test Tomato Eggs',
    'steps': '1. Beat eggs\\n2. Fry tomatoes\\n3. Mix',
    'ingredients': 'Tomato, Egg, Salt',
    'is_public': 'on'
}, follow_redirects=True)
assert res.status_code == 200
# Depending on UTF-8 handling in test response, checking exact bytes of 'Test Tomato Eggs' should work because it's ascii
assert b'Test Tomato Eggs' in res.data, "Recipe detail page didn't show newly created title"
assert b'Tomato' in res.data, "Ingredient missing"
print("OK Create recipe works.")

print("[5] Testing Ingredient Search (GET /search/ingredients)...")
res = client.get('/search/ingredients?items=Egg', follow_redirects=True)
assert res.status_code == 200
assert b'Test Tomato Eggs' in res.data, "Ingredient search didn't find the recipe containing 'Egg'"
print("OK Ingredient Search works.")

print("[6] Testing Recipe Update (POST /recipe/1/edit)...")
res = client.post('/recipe/1/edit', data={
    'title': 'Upgraded Tomato Eggs',
    'steps': '1. Beat eggs carefully...',
    'ingredients': 'Tomato, Egg, Salt, Scallion',
    'is_public': 'on'
}, follow_redirects=True)
assert res.status_code == 200
assert b'Upgraded Tomato Eggs' in res.data
print("OK Update recipe works.")

print("[7] Testing Recipe Delete (POST /recipe/1/delete)...")
res = client.post('/recipe/1/delete', follow_redirects=True)
assert res.status_code == 200
print("OK Delete recipe works.")

print("--------------------------------------------------")
print("All MVP tests (Step 5 verification) passed successfully!")
sys.exit(0)
