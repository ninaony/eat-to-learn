import requests
#from bs4 import BeautifulSoup
from recipe_scrapers import scrape_html
from core.models import Recipe, Ingredient, Component, ComponentIngredient
from core.tools import recipe_component_extraction
from recipe_scrapers._exceptions import SchemaOrgException

# Not in use: links
RECIPE_FIELDS = [ "title", "author", "description", "keywords", "instructions", 
                 "instructions_list", "ingredients", "ingredient_groups",
                 "dietary_restrictions", "equipment", "nutrients",
                 "prep_time", "cook_time", "total_time",
                 "cuisine", "category", "cooking_method", "yields",
                 "canonical_url", "image", "ratings", "ratings_count", "language"
]

class RecipeParseError(Exception):
    pass

def get_blank_recipe():
    return {field: None for field in RECIPE_FIELDS}

def clip_recipe(response):

    # handles no content
    if not response:
        return None
    
    scraper = scrape_html(response.content,  org_url=response.request.url)

    # handles no substantive content
    # TO DO: Still create a recipe draft but add warning message about incomplete required fields
    if not scraper.instructions() or not scraper.ingredients() or not scraper.title():
        return "No recipe content exists"
    
    if Recipe.objects.filter(name=scraper.title()).exists():
        return "Recipe already exists"

    recipe_data = get_blank_recipe()

    for field in recipe_data:
        try:
            method = getattr(scraper, field)
            recipe_data[field] = method()
        except (SchemaOrgException, AttributeError):
            # Fallback to None if schema data is missing or method doesn't exist
            recipe_data[field] = None

    
    # TO DO: return helper message if necessary
    return create_recipe(recipe_data)

# TO DO: Once I understand React logic
def add_recipe_manual(response):
    pass

def create_recipe(recipe_data: dict):
    recipe = Recipe.objects.create(name=recipe_data["title"], description=recipe_data["description"], 
                                          og_url=recipe_data["canonical_url"],image=recipe_data["image"], 
                                          instructions=recipe_data["instructions_list"], prep_time=recipe_data["prep_time"], 
                                          cook_time=recipe_data["cook_time"], total_time=recipe_data["total_time"])
   
   
    #ingredients_by_id = [{index : ingredient} for index, ingredient in enumerate(scraper.ingredients())]
   
    #TO DO: async for the llm call or return log error
    #components = recipe_component_extraction(scraper.title(), scraper.description(), 
                                   #scraper.instructions(), scraper.ingredient_groups(), 
                                    #ingredients_by_id)
    '''
       for component in components:
           for id in components['ingredient_list']:
   
               if Ingredient.objects.filter(name=ingredients_by_id.get):
   
    '''
     #yields=scraper.__getattribute__("recipeYield", None),cuisine=scraper.cuisine()
      
    return recipe

def edit_recipe():
    pass

def delete_recipe():
    pass


if __name__ == "__main__":

    url = 'https://www.gimmesomeoven.com/chipotle-chicken/'

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    recipe = recipe_parser(response)
    if type(recipe) == str:
        print(recipe)
    else:
        print(recipe.__dict__)
   

 





