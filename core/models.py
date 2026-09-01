from django.db import models


# Create your models here.

class Ingredient(models.Model):
    #id
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    

