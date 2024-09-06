from rest_framework import permissions


class RecipePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('DELETE', 'PATCH'):
            user = request.user
            return (user.is_authenticated
                    and (obj.author == user or user.is_staff))
        return True
