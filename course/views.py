from django.core.cache import cache
from django.db.models import Count
from rest_framework import viewsets,permissions,generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.throttling import UserRateThrottle
from django.utils import timezone
from django_redis import get_redis_connection
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *
from notification.tasks import *



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related('instructor').prefetch_related('videos').order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['level','category','status','price']
    searce_fields = ['title','description']
    ordering_fields = ['created_at','price','title']

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destry']:
            return [IsInstructorOrAdmin]
        return super().get_permissions()


class UserEnrolledCourseView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related('course')


class RecommendedCourseView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        key = f'recommend_{self.request.user.id}'
        cached_data = cache.get(key)
        if cached_data:
            return cached_data

        courses = Course.objects.annotate(num_students=Count('enrollment')).filter(Status='published').order_by('-num_students')[:5]
        cache.set(key,courses,60*10)
        return courses


class CreateInvoiceView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        course_id =self.request.data.get('course')
        course = get_object_or_404(Course,id=course_id,status=Course.Status.PUBLISHED)
        existing_invoice = Invoice.objects.filter(user=self.request.user,course=course,status=Invoice.Status.PENDING).first()
        if existing_invoice:
            serializer.instance = existing_invoice
        else:
            serializer.save(user=self.request.user,course=course,amount=course.price)
            send_notification_task.delay(
                user_id = self.request.user.id,
                title = 'صدور فاکتور جدید',
                message = f' برای دوره{course.title} فاکتور جدید ایجاد شد',
            )

class PayInvoiceView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self,request,invoice_id):
        invoice = get_object_or_404(Invoice,id=invoice_id,user=self.request.user,status=Invoice.Status.PENDING)

        fake_reference_code = f'11:25:34.10:02:1403'
        invoice.mark_maid(fake_reference_code)

        Enrollment.objects.get_or_create(user=request.user,course=invoice.course)

        send_notification_task.delay(
                user_id = self.request.user.id,
                title = 'پرداخت موفقیت آمیز بود ',
                message = f'پرداخت برای خرید دوره {invoice.id} موفقیت آمیز بود'
            )




        return Response({'detaild':'پرداخت با موفقیت انجام شد','payment_reference':fake_reference_code})