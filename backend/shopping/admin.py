from django.contrib import admin

from .models import ShoppingList


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_recipe_ingredients')
    search_fields = ('user__username',)  # Поиск по имени пользователя

    def get_recipe_ingredients(self, obj):
        return ", ".join(
            [str(ingredient) for ingredient in obj.recipe_ingredients.all()]
        )
    get_recipe_ingredients.short_description = 'Ингредиенты'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user').prefetch_related(
            'recipe_ingredients'
        )
        return queryset


admin.site.register(ShoppingList, ShoppingListAdmin)
