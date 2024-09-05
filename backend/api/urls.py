from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .user_views import FoodUserViewSet, AvatarViewSet
from .subscribe_views import SubscriptionViewSet
from .views import TagViewSet, IngredientViewSet, RecipeViewSet


router = DefaultRouter()
router.register(r'users', FoodUserViewSet, basename='user')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/me/avatar/',
        AvatarViewSet.as_view({'put': 'update', 'delete': 'delete_avatar'})
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscriptionViewSet.as_view({'post': 'create', 'delete': 'delete'})
    ),
    path('auth/', include('djoser.urls.authtoken')),
]
