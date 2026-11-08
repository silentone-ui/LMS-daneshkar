import django_filters.rest_framework as filters
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .forms import *
from .models import *
from .serializers import *
from .throttle import StaffRateThrottle
from django.http import Http404
from .permissions import *


class ProfileFilter(filters.FilterSet):
    course_enrolled_min = filters.NumberFilter(
        field_name="course_enrollesd", lookup_expr="gte"
    )
    course_enrolled_max = filters.NumberFilter(
        field_name="course_enrolled", lookup_expr="lte"
    )
    rating_min = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    rating_max = filters.NumberFilter(field_name="rating", lookup_expr="lte")


class ProfilePagination(PageNumberPagination):
    page_size = 4
    page_query_param = "page_size"
    max_page_size = 10


@method_decorator(cache_page(60*5),name='dispatch')
class ProfileListView(ReadOnlyModelViewSet):
    throttle_classes : list = []
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsInstructorOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProfileFilter
    search_fields = ["full_name", "github_link"]
    ordering_fields = ["rating", "full_name"]
    ordering = ["-rating"]
    pagination_class = ProfilePagination


class ProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


@method_decorator(cache_page(3000), name="get")
class ProfileRetrieveUpdateDestroyview(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer






class ProfileNplusoneView(APIView):
    def get(self,request):
        profiles=Profile.objects.select_related('user')
        data = []

        for profile in profiles:
            data.append(
                {
                    'full_name' : profile.full_name,
                    'user' : profile.user.first_name,
                }
            )
        return Response(data)