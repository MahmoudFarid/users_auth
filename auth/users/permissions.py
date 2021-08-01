from rest_framework import permissions


class CurrentUserPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.pk == user.pk
