from rest_framework.routers import DefaultRouter
from django.urls import include,path
from .views import *
router = DefaultRouter()
router.register(r'courses',CourseViewSet,basename='courses')
urlpatterns =[
    path("payment/invoice/",CreateInvoiceView.as_view(),name='create-invoice'),
    path("payment/invoice/<int:invoice_id>",PayInvoiceView.as_view(),name='create-invoice'),
    path("my-enrollments/",UserEnrolledCourseView.as_view(),name='my-enrollments'),
    path("enroll/",RecommendedCourseView.as_view(),name='recommended-courses'),
    path('',include(router.urls))

]