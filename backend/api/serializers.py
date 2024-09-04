from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from .picture_field import PictureField


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        write_only=True
    )
    tags = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    image = PictureField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data['id']
            amount = ingredient_data['amount']
            ingredient = Ingredient.objects.get(id=ingredient_id)
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )

        for tag_id in tags_data:
            tag = Tag.objects.get(id=tag_id)
            recipe.tags.add(tag)

        return recipe
