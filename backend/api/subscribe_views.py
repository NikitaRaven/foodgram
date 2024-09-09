from rest_framework import viewsets, status
from rest_framework.response import Response

from subscriptions.models import Subscription
from .subscribe_serializers import (
    SubscriptionSerializer, GetUserSubscriptionSerializer
)
from .constants import SUB_NOT_FOUND


class SubscriptionViewSet(viewsets.GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'author': kwargs.get('id'),
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            author = serializer.validated_data.get('author')
            serializer = GetUserSubscriptionSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(
            user_id=request.user.id,
            author_id=kwargs.get('id'),
        )
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': SUB_NOT_FOUND},
                        status.HTTP_400_BAD_REQUEST)
