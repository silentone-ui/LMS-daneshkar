from rest_framework.permissions import BasePermission


class IsInstructorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and 
            (request.user.profile.role in ['instructor','staff'] or request.user.is_superuser)
        )