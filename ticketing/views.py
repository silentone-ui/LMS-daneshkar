from django.shortcuts import render
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from .permissions import *



class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related('student','assigned_to').prefetch_related('messages')
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(student=user)


    def perform_create(self, serializer):
        ticket = serializer.save(student=self.request.user)
        TicketMessage.objects.create(
            ticket = ticket,
            sender = self.request.user,
            message = self.request.data.get('message',''),
            is_admin_reply = False,
        )


class TicketMessageViewSet(viewsets.ModelViewSet):
    queryset = TicketMessage.objects.all().select_related('ticket','sender')
    serializer_class = TicketMessageSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self,serializer):
        ticket = self.get_object_or_404(Ticket,id=self.request.data.get('ticket'))
        msg = serializer.save(sender=self.request.user,ticket=ticket,is_admin_reply=self.request.user.is_staff)
