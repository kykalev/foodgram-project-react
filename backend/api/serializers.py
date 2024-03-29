import base64
import logging

from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from recipes.models import (AmountIngredient, FavoriteRecipe, Ingredient,
                            Recipe, ShoppingList, Tag)
from user.models import CustomUser, Follow

logger = logging.getLogger()


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
                                         author=obj).exists()
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


class RecipeSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор - список рецептов без ингридиентов."""
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowCreateDeleteSerializer(serializers.ModelSerializer):
    """Подписка и отписка на автора."""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def validate(self, obj):
        if (self.context['request'].user == obj):
            raise serializers.ValidationError({'errors': 'Ошибка подписки.'})
        return obj

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(user=user,
                                         author=obj).exists()
        return False

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribeListSerializer(serializers.ModelSerializer):
    """Список авторов на которых подписан пользователь."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(user=user,
                                         author=obj).exists()
        return False

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            try:
                recipes = recipes[:int(limit)]
            except TypeError:
                logger.warning('limit должен иметь тип int')
        serializer = RecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data


class PasswordSerializer(serializers.Serializer):
    """Сериализатор смены пароля"""
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


class AmountIngredientCreateSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор. Ингредиент с количеством для рецепта."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


class AmountIngredientListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('amount',)


class RecipeListSerializer(serializers.ModelSerializer):
    """Список рецептов."""
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = AmountIngredientListSerializer(source='amountingredients',
                                                 many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteRecipe.objects.filter(user=user,
                                                 recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingList.objects.filter(user=user,
                                               recipe=obj).exists()
        return False


class RecipeCreateSerializer(RecipeListSerializer):
    """Создать, изменить, удалить рецепт."""
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = AmountIngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('is_favorited', 'is_in_shopping_cart')
        extra_kwargs = {
            'ingredients': {'required': True, 'allow_blank': False},
            'tags': {'required': True, 'allow_blank': False},
            'name': {'required': True, 'allow_blank': False},
            'text': {'required': True, 'allow_blank': False},
            'image': {'required': True, 'allow_blank': False},
            'cooking_time': {'required': True},
        }

    def validate(self, obj):
        if not obj.get('tags'):
            raise serializers.ValidationError(
                'Нужно указать минимум 1 тег.'
            )
        if not obj.get('ingredients'):
            raise serializers.ValidationError(
                'Нужно указать минимум 1 ингредиент.'
            )
        all_ingredients = [x.get('id') for x in obj.get('ingredients')]
        set_all_ingredients = set(all_ingredients)
        if len(set_all_ingredients) != len(all_ingredients):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться.'
            )
        ingredients_in_db = set(x[0] for x in list(Ingredient.objects.filter(
            id__in=set_all_ingredients).values_list('id')))
        missing = set_all_ingredients - ingredients_in_db
        if missing:
            raise serializers.ValidationError(
                f'Ингредиента(ов) с id {", ".join(map(str, missing))} нет')
        if not all(x.get('amount') > 0 for x in obj.get('ingredients')):
            raise serializers.ValidationError(
                'количество игредиента должно быть больше 0')
        return obj

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        recipe.tags.set(tags)
        results = []

        for ingredient in ingredients:
            ingredient_obj = get_object_or_404(Ingredient, id=ingredient['id'])
            amount = ingredient['amount']
            addition = AmountIngredient(
                recipe=recipe,
                ingredient=ingredient_obj,
                amount=amount
            )
            results.append(addition)
        AmountIngredient.objects.bulk_create(results)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        AmountIngredient.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            amount = ingredient['amount']
            AmountIngredient.objects.create(
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                recipe=instance, amount=amount
            )
        instance.save()
        instance.tags.set(tags)
        return instance

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance, context={"request": self.context.get('request')}
        ).data
