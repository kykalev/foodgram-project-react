from django.core.validators import MinValueValidator
from django.db import models

from user.models import CustomUser


class Tag(models.Model):
    """Модель Тегов."""
    name = models.CharField(verbose_name='Название тега', max_length=200)
    color = models.CharField(verbose_name='Цвет в HEX', max_length=7)
    slug = models.SlugField(verbose_name='Слаг тега', unique=True, max_length=7)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
    

class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(verbose_name='Название ингредиента',
                            max_length=200)
    measurement_unit = models.CharField(verbose_name='Мера',
                            max_length=200)


    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """Связующая модель ингредиентов и их количества."""
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='ingredients',
                                   verbose_name='Название ингредиента',
                                   on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента')


    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.amount} - {self.ingredient}'


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(CustomUser, verbose_name='Автор',
                               related_name='recipes',
                               on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(AmountIngredient,
                                         verbose_name='Ингредиенты',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='Теги')
    image = models.ImageField(verbose_name='Картинка рецепта',
                              upload_to='recipes/')
    name = models.CharField(verbose_name='Название рецепта',
                            max_length=200)
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1, message='Время приготовления не может быть меньше 1')]
        )
    pub_date = models.DateTimeField(verbose_name='Время публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):
    """ Модель избранного рецепта."""
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь',
                             related_name='favorites',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт',
                             related_name='favorites',
                             on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe.name} в избранных у {self.user.username}'


class ShoppingList(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь',
                             related_name='shopping_lists',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт',
                             related_name='shopping_lists',
                             on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'У {self.user.username} список покупок для {self.recipe.name}'
