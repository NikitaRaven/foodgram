import random
import string

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as django_filters

from recipes.models import Tag, Ingredient, Recipe
from .recipe_serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer
)
from .filters import IngredientFilter, RecipeFilter
from .permissions import RecipePermission


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('slug')
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
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
