from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient, Favorite
from shopping.models import ShoppingList
from .picture_field import PictureField
from .user_serializers import UserInfoSerializer
from .constants import NOT_DICT_INGREDIENT, NO_KEYS, DUPLICATE_ID


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        exclude = ('recipe', 'ingredient')


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
    author = UserInfoSerializer(read_only=True)
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
        exclude = ('short_link', 'created_at')

    def validate_ingredients(self, ingredients):
        seen_ids = set()
        for ingredient in ingredients:
            if not isinstance(ingredient, dict):
                raise serializers.ValidationError(NOT_DICT_INGREDIENT)
            if 'id' not in ingredient or 'amount' not in ingredient:
                raise serializers.ValidationError(NO_KEYS)

            ingredient_id = ingredient['id']
            if ingredient_id in seen_ids:
                raise serializers.ValidationError(DUPLICATE_ID, ingredient_id)
            seen_ids.add(ingredient_id)

        return ingredients

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        ingredients = [None] * len(ingredients_data)
        for i, ingredient_data in enumerate(ingredients_data):
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            serializer = RecipeIngredientSerializer(data={'amount': amount})
            serializer.is_valid(raise_exception=True)
            ingredients[i] = RecipeIngredient(
                recipe=recipe, ingredient=ingredient, amount=amount
            )
        RecipeIngredient.objects.bulk_create(ingredients)

        tags = Tag.objects.filter(id__in=tags_data)
        recipe.tags.set(tags)

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
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists() if request.user.is_authenticated else False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return ShoppingList.objects.filter(
            user=request.user, recipe=obj
        ).exists() if request.user.is_authenticated else False


class FavoriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = PictureField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = '__all__'
        extra_kwargs = {
            'recipe': {'write_only': True},
            'user': {'write_only': True}
        }


class ShoppingListSerializer(FavoriteSerializer):

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingList
