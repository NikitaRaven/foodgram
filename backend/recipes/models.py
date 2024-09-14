from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

import recipes.constants as const


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=const.TAG_NAME_LENGTH,
        unique=True,
        verbose_name=const.VERBOSE_NAME_TAG)
    slug = models.SlugField(
        max_length=const.TAG_NAME_LENGTH,
        unique=True,
        verbose_name=const.VERBOSE_SLUG_TAG,
    )

    class Meta:
        verbose_name = const.TAG_VERBOSE
        verbose_name_plural = const.TAG_VERBOSE_PLURAL

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=const.INGREDIENT_NAME_LENGTH,
        verbose_name=const.VERBOSE_NAME_INGREDIENT
    )
    measurement_unit = models.CharField(
        max_length=const.INGREDIENT_UNIT_LENGTH,
        verbose_name=const.VERBOSE_UNIT_INGREDIENT
    )

    class Meta:
        verbose_name = const.INGREDIENT_VERBOSE
        verbose_name_plural = const.INGREDIENT_VERBOSE_PLURAL

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=const.VERBOSE_AUTHOR_RECIPE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name=const.VERBOSE_INGREDIENTS_RECIPE
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name=const.VERBOSE_TAGS_RECIPE
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        default=None,
        verbose_name=const.VERBOSE_IMAGE_RECIPE
    )
    name = models.CharField(
        max_length=const.RECIPE_NAME_LENGTH,
        verbose_name=const.VERBOSE_NAME_RECIPE
    )
    text = models.TextField(verbose_name=const.VERBOSE_TEXT_RECIPE)
    cooking_time = models.PositiveIntegerField(
        verbose_name=const.VERBOSE_TIME_RECIPE,
        validators=(
            MinValueValidator(const.RECIPE_TIME_MIN, const.TIME_LOW),
            MaxValueValidator(const.RECIPE_TIME_MAX, const.TIME_HIGH)
        )
    )
    short_link = models.CharField(
        max_length=const.RECIPE_LINK_LENGTH,
        default='',
        verbose_name=const.VERBOSE_LINK_RECIPE
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=const.VERBOSE_DATE_RECIPE
    )

    class Meta:
        verbose_name = const.RECIPE_VERBOSE
        verbose_name_plural = const.RECIPE_VERBOSE_PLURAL

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name=const.VERBOSE_RECIPE_RI
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name=const.VERBOSE_INGREDIENT_RI
    )
    amount = models.PositiveIntegerField(
        verbose_name=const.VERBOSE_AMOUNT_RI,
        validators=(
            MinValueValidator(const.RI_AMOUNT_MIN, const.AMOUNT_LOW),
            MaxValueValidator(const.RI_AMOUNT_MAX, const.AMOUNT_HIGH)
        )
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')
        verbose_name = const.RI_VERBOSE
        verbose_name_plural = const.RI_VERBOSE_PLURAL


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=const.VERBOSE_USER_FAVORITE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=const.VERBOSE_RECIPE_FAVORITE
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = const.FAVORITE_VERBOSE
        verbose_name_plural = const.FAVORITE_VERBOSE_PLURAL
