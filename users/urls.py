import django_filters.rest_framework as filter
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.filters import BaseFilterBackend
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"profiles", ProfileView, basename="profiles-viewset")

# urlpatterns = [
#     path('profilelist/',ProfileListView.as_view(),name='profiles'),
#     path('detail/<int:pk>/',ProfileDetailView.as_view(),name='profile-detail'),
#     path('subscribe/',subscribe,name='subscribe')
# ]

# urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns = [
    path("fbv/Profiles/", profile_list, name="fbv-profiles"),
    path(
        "cbv/Profiles/",
        ProfileListView.as_view({"get": "list"}),
        name="cbv-profiles",
    ),
    path(
        "generics/profiles/",
        ProfileListCreateView.as_view(),
        name="generics-profile-list",
    ),
    path(
        "generics/profiles/<int:pk>/",
        ProfileRetrieveUpdateDestroyview.as_view(),
        name="generics-profiles-detail",
    ),
    path("viewset/", include(router.urls)),
    path(
        "nplusone/profiles",
        ProfileNplusoneView.as_view(),
        name="cached-profiles",
    )
]
