from django.shortcuts import render
from rest_framework import viewsets
from .models import Ingredient
#from django.core import serializers
from django.http import JsonResponse
from .serializers import IngredientSerializer
import requests


from .recipes import recipe_parser, RecipeParseError

# Create your views here.
#class IngredientViewSet(viewsets.ModelViewSet):
    #queryset = Ingredient.objects.all()
    #serializer_class = IngredientSerializer*/

def get_ingredients(request):
    name = request.GET.get('name') #None if not provided
    if name:
        ingredients = Ingredient.objects.filter(name__icontains=name)
    else:
        ingredients = Ingredient.objects.all()

    serializer = IngredientSerializer(ingredients, many=True)  # many=True because it's a queryset, not one object

    return JsonResponse(serializer.data, safe=False)
    #return JsonResponse(serializers.serialize("json", ingredients))
    #return JsonResponse(ingredients.list())
    #return serializers.serialize("json", ingredients)
    #return Ingredient.objects.raw('SELECT * FROM core_ingredient')

def fetch_recipe(request):
    site = request.GET.get("site")

    if not site:
        error_data = {"status": 400, 
                      "code": "MISSING_SITE_URL", 
                      "message": "Missing site field"} 
        return JsonResponse(error_data, status=400)


    # Handles network phase
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(site, timeout=10, headers=headers) # extract content from website 
        response.raise_for_status()

    except requests.exceptions.Timeout:
        error_data = {"status": 502, 
                       "code": "TIMEOUT", 
                       "message": "The request timed out"}
        return JsonResponse(error_data, status=502)
    
    except requests.exceptions.ConnectionError:
        error_data = {"status": 502, 
                      "code": "CONNECTION_ERROR", 
                      "message": "No connection established to site"} 
        return JsonResponse(error_data, status=502)
    
    except requests.exceptions.RequestException as e:

        # catch all for all other errors
        if e.response is None:
            error_data = {"status": 502, 
                          "code": "CONNECTION_ERROR", 
                          "message": "Other connection error"} 
            return JsonResponse(error_data, status=502)

        status_code = e.response.status_code
        if status_code == 404:
            error_data = {"status": 404, 
                          "code": "SITE_NOT_FOUND", 
                          "message": "No site found"}
            return JsonResponse(error_data, status=404)
        #elif status_code == 500:
            #print("Internal server error.")


    # Handles recipe parsing

    try:
        recipe_data = recipe_parser(response)
        if not recipe_data:
            error_data = {"status": 204, 
                                  "code": "NO_RECIPE", 
                                  "message": "No recipe found"}
            return JsonResponse(error_data, status=204)
        

    except RecipeParseError as e:
        error_data = {"status": 422, 
                      "code": "RECIPE_PARSE_ERROR", 
                      "message": "No site found"}
        return JsonResponse(error_data, status=422)
    
    return JsonResponse(recipe_data)   


    

