from django.shortcuts import render
from rest_framework import viewsets
from .models import Ingredient
#from django.core import serializers
from django.http import JsonResponse
from .serializers import IngredientSerializer

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
