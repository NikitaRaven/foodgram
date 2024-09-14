from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import FoodUser


class FoodUserAdmin(UserAdmin):
    model = FoodUser
    list_display = (
        'email', 'username', 'first_name', 'last_name', 'is_staff'
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar', )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'avatar')}),
    )


admin.site.register(FoodUser, FoodUserAdmin)
