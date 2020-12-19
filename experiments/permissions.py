from rest_framework.permissions import BasePermission

SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]


class IsStaffOrReadOnly(BasePermission):
    """
    The request is authenticated as staff user, or is a read-only request form authenticated user.
    """

    def has_permission(self, request, view):
        if request.user.is_staff or (request.method in SAFE_METHODS and request.user.is_authenticated):
            return True
        return False
