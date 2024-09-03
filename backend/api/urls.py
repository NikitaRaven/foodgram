from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .user_views import FoodUserViewSet, AvatarViewSet
from .views import TagViewSet, IngredientViewSet


router = DefaultRouter()
router.register(r'users', FoodUserViewSet, basename='user')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/me/avatar/',
        AvatarViewSet.as_view({'put': 'update', 'delete': 'delete_avatar'})
    ),
    path('auth/', include('djoser.urls.authtoken')),
]
