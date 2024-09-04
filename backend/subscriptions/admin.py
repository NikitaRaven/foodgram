from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user__username', 'author__username')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'author')


admin.site.register(Subscription, SubscriptionAdmin)
