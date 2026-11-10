from celery import shared_task
from django.contrib.auth import get_user_model


User = get_user_model()

@shared_task
def send_ticket_notification(receiver_id,message):
    if receiver_id:
        user =User.objects.filter(id=receiver_id).first()
        if user and user.phone:
            #send sms
            pass
        else:
            admins = User.objects.filter(is_stadd=True)
            for admin in admins:
                if admin.phone:
                    #send sms
                    pass
