from django.contrib import admin
from core.models import Ingredient, IngredientCategory
from core.models import Component, ComponentCategory, ComponentIngredient
from core.models import Recipe, RecipeCategory, Cuisine, Technique


# Register your models here.
admin.site.register(Ingredient)
admin.site.register(IngredientCategory)

admin.site.register(Component)
admin.site.register(ComponentCategory)
admin.site.register(ComponentIngredient)

admin.site.register(Recipe)
admin.site.register(RecipeCategory)
admin.site.register(Cuisine)
admin.site.register(Technique)
