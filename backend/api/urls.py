from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from .views import *

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register(r'users', UserViewSet, basename='users')
router_api.register(r'tags', TagViewSet, basename='tags')
router_api.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_api.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    # path('users/set_password/', SetPasswordView.as_view(),
    #      name='set_password'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),    
    path('', include(router_api.urls)),
]