import random
import string
from collections import defaultdict

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as django_filters

from recipes.models import Tag, Ingredient, Recipe, Favorite
from shopping.models import ShoppingList
from .recipe_serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteSerializer,
    ShoppingListSerializer
)
from .filters import IngredientFilter, RecipeFilter
from .permissions import RecipePermission


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('slug')
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('name')
    serializer_class = RecipeSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, RecipePermission
    )
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('GET',), url_path='get-link')
    def get_link(self, request, *args, **kwargs):
        recipe = self.get_object()
        random_sequence = ''.join(random.choices(string.ascii_lowercase, k=4))
        existing_recipe = Recipe.objects.filter(
            short_link=random_sequence
        ).first()

        if existing_recipe:
            existing_recipe.short_link = ''
            existing_recipe.save()

        recipe.short_link = random_sequence
        recipe.save()
        short_link = request.build_absolute_uri(f'/s/{recipe.short_link}')
        return Response({"short-link": short_link}, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=('GET',),
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request, *args, **kwargs):
        shopping_lists = ShoppingList.objects.filter(
            user=request.user
        ).prefetch_related(
            Prefetch('recipe__recipe_ingredients__ingredient')
        ).values_list(
            'recipe__recipe_ingredients__ingredient__name',
            'recipe__recipe_ingredients__amount',
            'recipe__recipe_ingredients__ingredient__measurement_unit'
        )

        ingredient_list = defaultdict(lambda: (0, ''))
        for key, value, unit in shopping_lists:
            ingredient_list[key] = (ingredient_list[key][0] + value, unit)
        ingredient_list = dict(sorted(ingredient_list.items()))

        response = HttpResponse(
            content_type='text/plain', status=status.HTTP_200_OK
        )
        response['Content-Disposition'] = 'attachment; filename="ingredients.txt"'
        for key, (value, unit) in ingredient_list.items():
            response.write(f'{key}: {value} {unit}\n')
        return response


class ShortLinkView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, random_sequence):
        recipe = Recipe.objects.filter(short_link=random_sequence).first()
        if recipe:
            serializer = RecipeSerializer(recipe,
                                          context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"detail": "Not found."},
                            status.HTTP_404_NOT_FOUND)


class FavoriteView(generics.GenericAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    not_found = 'The recipe is not in favorites.'

    def post(self, request, *args, **kwargs):
        data = {
            'recipe': kwargs.get('id'),
            'user': request.user.id
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe.objects.all(), id=kwargs.get('id'))
        instance = self.get_queryset().filter(
            recipe=recipe
        ).first()
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': self.not_found},
                        status.HTTP_404_NOT_FOUND)


class ShoppingListView(FavoriteView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    not_found = 'The recipe is not in shopping cart.'
