from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import FoodUser
from subscriptions.models import Subscription
from .picture_field import PictureField


class PostFoodUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Username must be alphanumeric and can contain @, ., +, - characters.',
            ),
            UniqueValidator(
                queryset=FoodUser.objects.all(),
                message='user with this username already exists.'
            )
        )
    )

    class Meta:
        model = FoodUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = FoodUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AvatarSerializer(serializers.ModelSerializer):
    avatar = PictureField(required=True)

    class Meta:
        model = FoodUser
        fields = ('avatar',)


class GetFoodUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(
        'get_avatar_url',
        read_only=True,
    )
    is_subscribed = serializers.SerializerMethodField(
        'get_is_subscribed',
        read_only=True,
    )

    class Meta:
        model = FoodUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'avatar'
        )

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, author=obj
            ).exists()
        return False


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        fields = ('current_password', 'new_password')

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')

        if not user.check_password(current_password):
            raise serializers.ValidationError({'current_password': 'Incorrect current password.'})

        if current_password == new_password:
            raise serializers.ValidationError({'new_password': 'New password must not be the same as the current password.'})

        return attrs
