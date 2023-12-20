from rest_framework.permissions import BasePermission


class IsSuperAdminOrReadOnly(BasePermission):
    """get: allowAny. post/put/del: isSuperAdmin
    """
    def has_permission(self, request, view):
        if request.method.lower() == 'get':
            return True
        return request.user.is_super_admin


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_admin)


class IsAdminOrAuthenticated(BasePermission):
    """get: authenticated. post/put/del: isAdmin
    """
    def has_permission(self, request, view):
        if request.method.lower() == 'get':
            return request.user.id
        return request.user.is_admin
