from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """
    Проверяет, является ли пользователь активным сотрудником
    для доступа к представлениям
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_active
