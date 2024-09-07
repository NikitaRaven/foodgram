from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient, Favorite
from shopping.models import ShoppingList
from .picture_field import PictureField
from .user_serializers import GetFoodUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'ingredient', 'amount')
        extra_kwargs = {'ingredient': {'write_only': True}}


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        write_only=True,
        allow_empty=False,
    )
    tags = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        allow_empty=False
    )
    image = PictureField(required=True)
    author = GetFoodUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(
        'get_is_favorited',
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def validate_ingredients(self, ingredients):
        seen_ids = set()
        for ingredient in ingredients:
            if not isinstance(ingredient, dict):
                raise serializers.ValidationError("Each ingredient must be a dictionary.")
            if 'id' not in ingredient or 'amount' not in ingredient:
                raise serializers.ValidationError("Each ingredient must contain 'id' and 'amount'.")
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError("Amount must be greater than zero.")

            ingredient_id = ingredient['id']
            if ingredient_id in seen_ids:
                raise serializers.ValidationError(f"Duplicate ingredient id found: {ingredient_id}.")
            seen_ids.add(ingredient_id)

        return ingredients

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        ingredients = Ingredient.objects.all()
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            ingredient = get_object_or_404(ingredients, id=ingredient_id)
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )

        tags = Tag.objects.all()
        for tag_id in tags_data:
            tag = get_object_or_404(tags, id=tag_id)
            recipe.tags.add(tag)

        return recipe

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(
            instance.tags.all(), many=True
        ).data
        representation['ingredients'] = RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=instance).select_related(
                'ingredient'
            ), many=True
        ).data
        return representation

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Favorite.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return ShoppingList.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = PictureField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('id', 'recipe', 'user', 'name', 'image', 'cooking_time')
        extra_kwargs = {
            'recipe': {'write_only': True},
            'user': {'write_only': True}
        }


class ShoppingListSerializer(FavoriteSerializer):

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingList
