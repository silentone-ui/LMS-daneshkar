from django.contrib.auth import login, logout
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.throttling import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsOwner, IsStaffUser
from .serializers import *


class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)
        return user


class CustomLoginApiView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated & IsOwner & IsStaffUser]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({"detail": "کاربر با موفقیت خارج شد"}, status=200)
        except Exception:
            return Response({"detail": "توکن اشتباه بود"}, status=400)
