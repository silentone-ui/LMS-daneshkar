from rest_framework import permissions

class IsInstructorOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        profile = getattr(user,'profile',None)
        if not profile:
            return False
        return profile.role in ['instructor','staff']
