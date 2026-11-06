from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path("api/auth/register/", RegisterApiView.as_view(), name="register"),
    path("api/auth/login/", CustomLoginApiView.as_view(), name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/logout/", LogoutApiView.as_view(), name="logout"),
]
