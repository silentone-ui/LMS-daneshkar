from django.urls import path,include
from .views import *


urlpatterns = [
    path('',NotificationListView.as_view(),name='notification-list')
]