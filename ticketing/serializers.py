from rest_framework import serializers
from .models import *

class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = '__all__'
        read_only_fields = ['sender','ticket','created_at']


class TicketSerializer(serializers.ModelSerializer):
    messages = TicketMessageSerializer(many=True,read_only=True)

    class Meta:
        model = Ticket
        fields = ['id','student','subject','assigned_to','created_at','messages']
        read_only_fields = ['student','created_at']