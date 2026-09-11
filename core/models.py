from django.db import models
from django.conf import settings


NAME_LENGTH = 50


## Ingredient fields
class IngredientCategory(models.Model):
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

    class Meta:
        verbose_name_plural = "Ingredient Categories"

class Ingredient(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True,blank=True)


## Component fields
class ComponentCategory(models.Model):
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

    class Meta:
        verbose_name_plural = "Component Categories"

class Component(models.Model):
    name =  models.CharField(max_length=NAME_LENGTH, unique=True)
    category = models.ForeignKey(ComponentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through="ComponentIngredient",related_name="components")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="outputs")
    #yields = models.PositiveIntegerField(null=True)

class ComponentIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)



## Recipe fields
class RecipeCategory(models.Model):
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

    class Meta:
        verbose_name_plural = "Recipe Categories"

class Cuisine(models.Model):
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

class Technique(models.Model):
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

class Recipe(models.Model):
    name= models.CharField(max_length=NAME_LENGTH, unique=True)
    description = models.CharField(max_length=300, blank=True)
    og_url = models.URLField(max_length=300, blank=True)
    image = models.ImageField(upload_to="recipes/", blank=True)

    instructions = models.JSONField(default=list)
    #ingredients handled in component model-> outputs

    prep_time = models.PositiveIntegerField(null=True, blank=True)
    cook_time = models.PositiveIntegerField(null=True, blank=True)
    total_time = models.PositiveIntegerField(null=True, blank=True)
    yields = models.PositiveIntegerField(null=True, blank=True)

    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(RecipeCategory, blank=True)
    techniques = models.ManyToManyField(Technique,blank=True)

    # ADD USER LATER
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="recipes")

    #deleting results in this being False (in order to perserve components for old meals)
    is_active = models.BooleanField(default=True)



## Meal fields - TO DO LATER
'''class MealComponentRole(models.Model):
    name= models.CharField(max_length=NAME_LENGTH, unique=True)

class MealComponent(models.Model):
    meal = models.ManyToManyField(through="Meal", related_name="components")
    component = models.ManyToManyField(Component)
    #unique meal-component pairing thing (meta class)
    role = models.ForeignKey(MealComponentRole, on_delete=models.PROTECT)

class MealPattern(models.Model):
    name= models.CharField(max_length=NAME_LENGTH, unique=True)

class Meal(models.Model):
    name = models.CharField(max_length=NAME_LENGTH, unique=True)
    pattern = models.ForeignKey()
'''




    

