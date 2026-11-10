from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('tickets',TicketViewSet,basename='ticket')
router.register('messages',TicketMessageViewSet,basename='message')

urlpatterns = [
    path('',include(router.urls))
]