from django.db import models
from django.contrib.auth import get_user_model

from .constants import (
    TAG_NAME_LENGTH, VERBOSE_NAME_TAG, VERBOSE_SLUG_TAG, TAG_VERBOSE,
    TAG_VERBOSE_PLURAL, INGREDIENT_NAME_LENGTH, INGREDIENT_UNIT_LENGTH,
    VERBOSE_NAME_INGREDIENT, VERBOSE_UNIT_INGREDIENT, INGREDIENT_VERBOSE,
    INGREDIENT_VERBOSE_PLURAL, RECIPE_NAME_LENGTH, RECIPE_LINK_LENGTH,
    VERBOSE_AUTHOR_RECIPE, VERBOSE_INGREDIENTS_RECIPE, VERBOSE_TAGS_RECIPE,
    VERBOSE_IMAGE_RECIPE, VERBOSE_NAME_RECIPE, VERBOSE_TEXT_RECIPE,
    VERBOSE_TIME_RECIPE, VERBOSE_LINK_RECIPE, VERBOSE_DATE_RECIPE,
    RECIPE_VERBOSE, RECIPE_VERBOSE_PLURAL, VERBOSE_RECIPE_RI,
    VERBOSE_INGREDIENT_RI, VERBOSE_AMOUNT_RI, RI_VERBOSE, RI_VERBOSE_PLURAL,
    VERBOSE_USER_FAVORITE, VERBOSE_RECIPE_FAVORITE, FAVORITE_VERBOSE,
    FAVORITE_VERBOSE_PLURAL
)


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_NAME_LENGTH,
        unique=True,
        verbose_name=VERBOSE_NAME_TAG)
    slug = models.SlugField(
        max_length=TAG_NAME_LENGTH,
        unique=True,
        verbose_name=VERBOSE_SLUG_TAG,
    )

    class Meta:
        verbose_name = TAG_VERBOSE
        verbose_name_plural = TAG_VERBOSE_PLURAL

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=INGREDIENT_NAME_LENGTH,
        verbose_name=VERBOSE_NAME_INGREDIENT
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_UNIT_LENGTH,
        verbose_name=VERBOSE_UNIT_INGREDIENT
    )

    class Meta:
        verbose_name = INGREDIENT_VERBOSE
        verbose_name_plural = INGREDIENT_VERBOSE_PLURAL

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=VERBOSE_AUTHOR_RECIPE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name=VERBOSE_INGREDIENTS_RECIPE
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name=VERBOSE_TAGS_RECIPE
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        default=None,
        verbose_name=VERBOSE_IMAGE_RECIPE
    )
    name = models.CharField(
        max_length=RECIPE_NAME_LENGTH,
        verbose_name=VERBOSE_NAME_RECIPE
    )
    text = models.TextField(verbose_name=VERBOSE_TEXT_RECIPE)
    cooking_time = models.PositiveIntegerField(
        verbose_name=VERBOSE_TIME_RECIPE
    )
    short_link = models.CharField(
        max_length=RECIPE_LINK_LENGTH,
        default='',
        verbose_name=VERBOSE_LINK_RECIPE
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=VERBOSE_DATE_RECIPE
    )

    class Meta:
        verbose_name = RECIPE_VERBOSE
        verbose_name_plural = RECIPE_VERBOSE_PLURAL

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name=VERBOSE_RECIPE_RI
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name=VERBOSE_INGREDIENT_RI
    )
    amount = models.PositiveIntegerField(verbose_name=VERBOSE_AMOUNT_RI)

    class Meta:
        unique_together = ('recipe', 'ingredient')
        verbose_name = RI_VERBOSE
        verbose_name_plural = RI_VERBOSE_PLURAL


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=VERBOSE_USER_FAVORITE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=VERBOSE_RECIPE_FAVORITE
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = FAVORITE_VERBOSE
        verbose_name_plural = FAVORITE_VERBOSE_PLURAL
