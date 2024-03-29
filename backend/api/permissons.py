from rest_framework import permissions


class UserEditPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ('PUT', 'PATCH') and (
                not request.user.is_superuser):
            return False
        else:
            return True


class IsAuthorOrReadOnlyRecipePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
