from recipe_scrapers import scrape_html
from recipe_scrapers._exceptions import SchemaOrgException
from core.models import Recipe
from core.services.recipes import create_recipe

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
    # TO DO: Raise RecipeParseError
    # TO DO: Still create a recipe draft but add warning message about incomplete required fields
    if not scraper.instructions() or not scraper.ingredients():
        return "No recipe content exists"

    # TO DO: Add a check to see if there is a status marked draft  (retry)
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

    # TO DO: add draft status field just in case the user doesn't save it?
    # TO DO: return helper message if necessary
    return create_recipe(recipe_data)
