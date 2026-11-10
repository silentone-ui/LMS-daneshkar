from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import *
router = DefaultRouter()

router.register('lessons',LessonViewSet)
router.register('contents',LessonContentViewSet)


urlpatterns = [
    path('',include(router.urls))
]