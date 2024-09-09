from django.contrib import admin

from .models import ShoppingList


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
    list_filter = ('user', 'recipe')


admin.site.register(ShoppingList, ShoppingListAdmin)
