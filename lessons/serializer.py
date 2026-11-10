from rest_framework import serializers
from .models import *

class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContent
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    contents = LessonContentSerializer(many=True,read_only=True)

    class Meta:
        model = Lesson
        fields = ['id','course','title','order','contents']