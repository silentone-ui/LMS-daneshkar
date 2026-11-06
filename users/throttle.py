from rest_framework.throttling import UserRateThrottle


class StaffRateThrottle(UserRateThrottle):

    def allow_request(self, request, view):
        if (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        ):
            return True
        return super().allow_request(request, view)
