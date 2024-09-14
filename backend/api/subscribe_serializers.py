from rest_framework import serializers

from recipes.models import Recipe
from subscriptions.models import Subscription
from .user_serializers import UserInfoSerializer
from subscriptions.constants import SUB_YOURSELF


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class GetUserSubscriptionSerializer(UserInfoSerializer):
    recipes = serializers.SerializerMethodField(
        'get_recipes',
        read_only=True
    )
    recipes_count = serializers.SerializerMethodField(
        'get_recipes_count',
        read_only=True
    )

    class Meta(UserInfoSerializer.Meta):
        fields = UserInfoSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit', None)
        recipes = Recipe.objects.filter(author=obj)

        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]

        return SubscribeRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'

    def validate(self, attrs):
        if attrs['user'] == attrs['author']:
            raise serializers.ValidationError(SUB_YOURSELF)
        return super().validate(attrs)
