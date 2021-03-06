from yummly import Client
from Recipe import *
import StepScraper

TIMEOUT = 5.0
RETRIES = 0

client = Client(api_id = '0ad05d37', api_key = 'b616f863887a7d2cb6d4baf30cd3cbe2', timeout = TIMEOUT, retries = RETRIES)

allowed_recipe_sources = ["Pillsbury Brand", "Betty Crocker", "Tablespoon", "Life Made Delicious"]
def getFirstUseableRecipeId(params):
    results = client.search(**params)
    matches = results.matches
    for match in matches:
        if match.sourceDisplayName in allowed_recipe_sources:
            return match.id

def getAllUseableRecipes(search_term):
    good_matches = []
    for i in range(5):
        search_params = {
            'q': search_term,
            'start': i * 40,
            'maxResults': (i + 1) * 40,
            'requirePicutres': True
        }
        results = client.search(**search_params)
        matches = results.matches
        for match in matches:
            if match.sourceDisplayName in allowed_recipe_sources:
                good_matches.append(match)
    return good_matches

def getRecipeFromId(recipe_id):
    return client.recipe(recipe_id)

def getYummlyUrlFromRecipe(recipe):
    url = recipe.source.sourceRecipeUrl
    return url

def getRecipeClassFromId(recipe_id):
    recipe = getRecipeFromId(recipe_id)
    url = getYummlyUrlFromRecipe(recipe)
    steps = StepScraper.getStepsFromYummlyUrl(url)

    return Recipe(recipe.name, recipe.id, recipe.rating, recipe.ingredientLines, steps, recipe.images[0].hostedLargeUrl)

def getRecipe(search_term):
    search_params = {
        'q': search_term,
        'start': 0,
        'maxResults': 100,
        'requirePicutres': True
    }
    recipe_id = getFirstUseableRecipeId(search_params)
    if recipe_id == None:
        return None

    recipe = getRecipeFromId(recipe_id)
    url = getYummlyUrlFromRecipe(recipe)
    steps = StepScraper.getStepsFromYummlyUrl(url)

    return Recipe(recipe.name, recipe.id, recipe.rating, recipe.ingredientLines, steps, recipe.images[0].hostedLargeUrl)
