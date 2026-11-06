from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    full_name = models.CharField(max_length=300)

    class Role(models.TextChoices):
        STUDENT = "دانش آموز"
        INSTRUCTOR = "instructor"
        STAFF = "staff"

    role = models.CharField(
        max_length=50, choices=Role.choices, default=Role.STUDENT
    )
    avatar = models.ImageField(
        upload_to="profile-avatars/", blank=True, null=True
    )
    location = models.CharField(max_length=200, blank=True, null=True)
    course_enrolled = models.PositiveIntegerField(default=0, editable=False)
    course_completed = models.PositiveIntegerField(default=0, editable=False)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True, editable=False
    )

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها "
        ordering = ("-rating",)

    def __str__(self):
        return self.full_name
