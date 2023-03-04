from django.contrib import admin

from .models import Ingredient, Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_display_links = ('id',)
    list_filter = ('name', 'author', 'tags')
    list_editable = ('name', 'author')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id',)
    list_filter = ('name',)
    list_editable = ('name', 'measurement_unit')

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
