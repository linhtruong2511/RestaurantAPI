from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerUserID(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Chỉ được phép lấy tài khoản của chính tài khoản đăng nhập
        """
        return obj.id == request.user.id

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_staff
        )