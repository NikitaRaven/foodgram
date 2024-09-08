from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe
from .constants import (
    VERBOSE_USER, VERBOSE_RECIPE,
    SHOPPING_VERBOSE, SHOPPING_VERBOSE_PLURAL
)


User = get_user_model()


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name=VERBOSE_USER
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name=VERBOSE_RECIPE
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = SHOPPING_VERBOSE
        verbose_name_plural = SHOPPING_VERBOSE_PLURAL

    def __str__(self):
        return f'Корзина покупок для {self.user.username}'
