from celery import shared_task
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

@shared_task
def send_notification_task(user_id,title,message):
    try:
        user = User.objects.get(pk=user_id)
        Notification.objects.create(user=user,title=title,message=message)
    except User.DoesNotExist:
        pass