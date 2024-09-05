from rest_framework import serializers

from recipes.models import Recipe
from subscriptions.models import Subscription
from .user_serializers import GetFoodUserSerializer


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class GetUserSubscriptionSerializer(GetFoodUserSerializer):
    recipes = SubscribeRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta(GetFoodUserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count', 'avatar'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit', None)
        recipes = Recipe.objects.filter(author=obj)

        if recipes_limit is not None:
            recipes = recipes[:int(recipes_limit)]

        return SubscribeRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'author')

    def validate(self, attrs):
        if attrs['user'] == attrs['author']:
            raise serializers.ValidationError("You can't subscribe to yourself.")
        return super().validate(attrs)
