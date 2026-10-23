from core.models import Recipe, Ingredient, Component, ComponentIngredient
from core.tools import recipe_component_extraction

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
