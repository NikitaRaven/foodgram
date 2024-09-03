from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import RecipeIngredient


User = get_user_model()


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_list'
    )
    recipe_ingredients = models.ManyToManyField(
        RecipeIngredient, related_name='shopping_lists'
    )

    def __str__(self):
        return f'Shopping list for {self.user.username}'
