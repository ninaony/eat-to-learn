import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)

def recipe_component_extraction(recipe_title, recipe_description, 
                                recipe_instructions, ingredient_groups, 
                                ingredients_with_ids):
    

    client = _get_groq_client()

    output_format = '''The output should be in json format. We have a dictionary with one key called 'components'. 
    The value of that item is a list of dictionaries where each dictionary has two keys called 'name' and 'ingredient_list'. 
    The value for 'name' is a string corresponding to the name of the component that you will generate 
    based on what the recipe intends to create for that ingredient grouping. 
    The value for 'ingredient_list' is a list of integers, where each integer represents the 
    id of the ingredient belonging in that grouping. For each ingredient grouping (aka component) identified, 
    create a dictionary item with the name and the corresponding list of ingredients by id name. 
    All components names should be an object and specific to the recipe. For example if a grouping is identified as 
    "For the sauce", the name of the component should be called <something relating to recipe but short> Sauce. 
    Since it's a proper noun, every letter in the name should be capitalized. '''

    system_promt = f'''You will be analyzing recipes to parse out the ingredient groupings. 
    There are ingredient groupings provided, but you will be using that as a starting point. 
    Ingredient groupings within the recipe are called components. 
    For example, in a taco recipe the components may include the meat, the sauces, the tortilla, and toppings.
    Each part should be its own component, so I should end up with components for: the meat, each sauce is its own 
    component, tortilla, and the toppings as one component. 
    For toppings (maybe seen as an ingredient grouping called "for serving"), create a grouping with a 
    short version of the recipe name + 'toppings'.
    Only used information provided in the user prompt to parse the components. 
    This is the output format: {output_format}'''
    
    user_prompt = f'''These are the ingredient groupings to be verified {ingredient_groups}. 
    This is list of ingredients and their corresponding ids: {ingredients_with_ids}. 
    The folliwng information is the only information you can use to verify ingredient groupings: 
    recipe name - {recipe_title}, recipe description - {recipe_description}, recipe instructions - {recipe_instructions}.'''


    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_promt
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ], 
        model="openai/gpt-oss-120b"
                )
    # model alt: qwen/qwen3.6-27b

    response_string = response.choices[0].message.content
        #print("log: Nothing recieved")
        #return None

    response_json = json.loads(response_string)
    if not response_json.get('components'):
        print("log: Nothing recieved")
    

    return response_json.get('components')




