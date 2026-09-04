"""
URL configuration for eat_to_learn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from core.views import IngredientViewSet
from core.views import get_ingredients, fetch_recipe

#router = DefaultRouter()
#router.register(r'ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    #path('/', )
    path('admin/', admin.site.urls),
    path('ingredient/', get_ingredients),
    path('fetch/', fetch_recipe, name="fetch_recipe")
    #path('api/', include(router.urls)),
]
