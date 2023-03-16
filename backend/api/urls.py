from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register(r'users', UserViewSet, basename='users')
router_api.register(r'tags', TagViewSet, basename='tags')
router_api.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_api.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_api.urls)),
]
