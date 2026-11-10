from rest_framework import serializers
from . models import *

class CourseVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVideo
        fields = ['id','title','video_file','order']

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name',read_only=True)
    videos = CourseVideoSerializer(many=True,read_only=True)

    class Meta:
        model=Course
        fields = '__all__'
        read_only_fields = ['instructor','created_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course',read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['user','enrolled_at']
        


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['user','amount','status','created_at','payment_reference']