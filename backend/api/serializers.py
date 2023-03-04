import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import *
from user.models import *


class Base64ImageField(serializers.ImageField):
    """Кастомный тип поля для декодирования текст-картинка."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Пользователя."""
    class Meta:
        model = Сu
        fields = ('id', 'name', 'color', 'slug')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    pass


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    pass


class ShoppingListSerializer(serializers.ModelSerializer):
    pass