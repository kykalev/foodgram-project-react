from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель кастомного пользователя."""
    username = models.CharField(
        "Логин",
        max_length=150,
        unique=True,
        help_text=(
            f"Требуется 150 символов или меньше, "
            f"только буквы, цифры и @/./+/-/_."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": "Пользователь с таким именем пользователя уже есть.",
        },
    )
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    email = models.EmailField("Почта", max_length=254)
    password = models.CharField("Пароль", max_length=150)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['last_name']

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='follower', verbose_name='Подписчик')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='author', verbose_name='Автор')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow_model'
            )
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.author}."
