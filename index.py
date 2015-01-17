from flask import Flask, request
import sys
import os
from request_handler import request_handler
sys.path.insert(0, './recipes/')
import RecipeGetter
import json

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/recipe/get/first/<search:search>')
def create_recipe(search):
    return request_handler(RecipeGetter.getRecipe(search))

@app.route('/recipe/choose/<recipe_id:recipe_id>')
def choose_recipe(recipe_id):
    return request_handler(RecipeGetter.getRecipeFromId(recipe_id))

@app.route('/recipe/get/all/<search:search>')
def return_all_recipes(search):
    return RecipeGetter.getAllUseableRecipes(search)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/static/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('static', path))

@app.route('/request/ingredients/')
def request_ingredients():
    return json.dump(rh.get_recipe().get_ingredients_raw())

if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=5001)
