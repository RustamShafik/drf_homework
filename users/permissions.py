from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )


class IsOwnerOrModer(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.groups.filter(name="Модераторы").exists():
            return True
        return obj.owner == request.user
