from rest_framework.permissions import BasePermission


class IsSuperAdminOrReadOnly(BasePermission):
    """get: allowAny. post/put/del: isSuperAdmin
    """
    def has_permission(self, request, view):
        if request.method.lower() == 'get':
            return True
        return request.user.is_super_admin
