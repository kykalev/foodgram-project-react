import base64

from django.contrib.auth.models import User
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
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'email', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(user=user,
                                         subscribe=obj).exists()
        return False

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            **validated_data, password=self.initial_data['password']
        )
    
    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username указан неверно!')
        return data


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True)
    ingredients = TagSerializer(many=True)

    class Meta:
        model = Ingredient
        fields = ('ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time')


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    pass


class ShoppingListSerializer(serializers.ModelSerializer):
    pass