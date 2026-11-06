from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def manage_profile(sender, instance, created, **kwargs):
    full_name = f"{instance.first_name} {instance.last_name}".strip()
    if created:
        Profile.objects.create(user=instance, full_name=full_name)
    else:
        Profile.objects.update_or_create(
            user=instance, defaults={"full_name": full_name}
        )
