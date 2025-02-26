from rest_framework.permissions import BasePermission


class IsOwnerUserID(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Chỉ được phép lấy tài khoản của chính tài khoản đăng nhập
        """
        return obj.id == request.user.id