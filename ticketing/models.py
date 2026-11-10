from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Ticket(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tickets')
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User,null=True,blank=True,related_name='assigned_tickets',on_delete=models.SET_NULL)

    def __str__(self):
        return f'Ticket #{self.id} by {self.student}'

class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin_reply = models.BooleanField(default=False)

    def __str__(self):
        return f'Message by {self.sender} on ticket #{self.ticket.id}'