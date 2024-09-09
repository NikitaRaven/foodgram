from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .user_serializers import (
    UserCreateSerializer, UserInfoSerializer,
    AvatarSerializer, PasswordSerializer
)
from .subscribe_serializers import GetUserSubscriptionSerializer
from users.models import FoodUser


class FoodUserViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = FoodUser.objects.all().order_by('username')
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            if self.action == 'subscriptions':
                return GetUserSubscriptionSerializer
            return UserInfoSerializer

        if method == 'POST':
            if self.action == 'set_password':
                return PasswordSerializer
            return UserCreateSerializer

    @action(detail=False,
            methods=('GET',),
            url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
    def get_profile_info(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), id=request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False,
            methods=('POST',),
            permission_classes=(permissions.IsAuthenticated,))
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=('GET',),
            permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request, *args, **kwargs):
        authors = [sub.author for sub in request.user.subscriptions.all()]
        paginated_authors = self.paginate_queryset(authors)
        serializer = self.get_serializer(
            paginated_authors, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class AvatarViewSet(mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = FoodUser.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.request.user.id)

    def delete_avatar(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.avatar = None
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
