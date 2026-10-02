import requests
#from bs4 import BeautifulSoup
from recipe_scrapers import scrape_html
from .models import Recipe, Ingredient, Component, ComponentIngredient
from .tools import recipe_component_extraction

class RecipeParseError(Exception):
    pass

def recipe_parser(response):

    # handles no content
    if not response:
        return None

    # if schema
            # create new object 
            # parse data
            # store data in new objects
    
    scraper = scrape_html(response.content,  org_url=response.request.url)
    

    # handles no substantive content
    # potential human in the loop -> continue anyways, and they'll fill it manually?
    if not scraper.instructions() or not scraper.ingredients():
        return "No recipe content exists"
    
    if Recipe.objects.filter(name=scraper.title()).exists():
        return "Recipe already exists"

    
    new_recipe = Recipe.objects.create(name=scraper.title(), description=scraper.description(), 
                                       og_url=scraper.canonical_url(),image=scraper.image(), 
                                       instructions=scraper.instructions_list(), prep_time=scraper.prep_time(), 
                                       cook_time=scraper.cook_time(), total_time=scraper.total_time())


    ingredients_by_id = [{index : ingredient} for index, ingredient in enumerate(scraper.ingredients())]

    # TO DO: get ingredient category information from LLM simultaneously
    # TO DO: quantity and ingredient separation
    # TO DO: what if LLM generates similar component names -> rn component names are set to unique
    components = recipe_component_extraction(scraper.title(), scraper.description(), 
                                scraper.instructions(), scraper.ingredient_groups(), 
                                 ingredients_by_id)

    



   
    #yields=scraper.__getattribute__("recipeYield", None),cuisine=scraper.cuisine()
    
    
     # if no schema 
            # use AI to parse schema 
            # move to stretch

     # Recipe schema exists     
    #if content.text..get("@type") == "Recipe":

        
     
    return new_recipe


if __name__ == "__main__":

    url = 'https://www.gimmesomeoven.com/chipotle-chicken/'

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    recipe = recipe_parser(response)
    if type(recipe) == str:
        print(recipe)
    else:
        print(recipe.__dict__)
   

 





