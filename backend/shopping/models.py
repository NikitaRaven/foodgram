from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe


User = get_user_model()


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_list'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_list'
    )

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'Shopping list for {self.user.username}'
