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

# def profile_list_view(request):
#     profiles = Profile.objects.select_related('user')
#     return render(request,'profile_list.html',{'profiles' : profiles})


# def profile_detail_view(request,pk):
#     profile = get_object_or_404(Profile,pk=pk)
#     return render(request,'profile-detail.html',{'profile':profile})


# class ProfileListView(ListView):
#     model = Profile
#     queryset = Profile.objects.select_related('user')
#     template_name = 'profile_list.html'
#     context_object_name = 'profiles'

# class ProfileDetailView(DetailView):
#     model = Profile
#     template_name = 'profile-detail.html'
#     context_object_name = 'profile'


# def subscribe(request):
#     if request.method == 'POST':
#         form = UsersForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             print('ثبت شد',email)
#     else:
#         form = UsersForm()

#     return render(request,'subscribe.html',{'form':form})


@api_view(["GET"])
def profile_list(request):
    profiles = Profile.objects.all()
    serializer_class = ProfileSerializer(profiles, many=True)
    return Response(serializer_class.data)


# class ProfileListView(APIView):
#     throttle_classes = []

#     def get(self,request):
#         profiles = Profile.objects.all()
#         serializer_class = ProfileSerializer(profiles,many=True)
#         return Response(serializer_class.data)


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


# @method_decorator(cache_page(60*5),name='dispatch')
class ProfileListView(ReadOnlyModelViewSet):
    throttle_classes : list = []
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
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


class ProfileView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


@receiver(post_save, sender=Profile)
def clear_profile_cache(sender, instance, **kwargs):
    cache.delete_pattern("views.decorators.cache*")




class ProfileTestViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk == 900:
            raise Http404("پروفایل پیدا نشد ")
        return super().retrieve(request,*args,**kwargs)



def profiles_list(request):
    profiles = Profile.objects.all()
    for profile in profiles:
        print(profile.user.first_name)


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