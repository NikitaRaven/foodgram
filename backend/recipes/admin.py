from django import forms
from django.contrib import admin

from .models import Tag, Ingredient, Favorite, Recipe, RecipeIngredient
from .constants import ADMIN_NO_INGREDIENTS


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
    list_filter = ('user', 'recipe')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user', 'recipe')
        return queryset


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('short_link',)

    def clean(self):
        cleaned_data = super().clean()
        total_forms = int(self.data.get('recipe_ingredients-TOTAL_FORMS', 0))

        has_ingredient = False
        for i in range(total_forms):
            ingredient = self.data.get(f'recipe_ingredients-{i}-ingredient')
            amount = self.data.get(f'recipe_ingredients-{i}-amount')
            if ingredient and amount:
                has_ingredient = True
                break

        if not has_ingredient:
            raise forms.ValidationError(ADMIN_NO_INGREDIENTS)

        return cleaned_data


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = ('name', 'author_username', 'get_favorite_count')
    search_fields = ('author__username', 'name')
    list_filter = ('tags',)
    inlines = (RecipeIngredientInline,)

    def author_username(self, obj):
        return obj.author.username
    author_username.short_description = 'Автор'

    def get_favorite_count(self, obj):
        return obj.favorites.count()
    get_favorite_count.short_description = 'Количество добавлений в избранное'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('author').prefetch_related(
            'tags', 'favorites'
        )
        return queryset


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Recipe, RecipeAdmin)
