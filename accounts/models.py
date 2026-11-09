from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
import  random
from django.utils import timezone



class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password=None, **extra_fields):
        first_name = extra_fields.get("first_name")
        last_name = extra_fields.get("last_name")
        if not last_name or not first_name:
            raise ValueError("The fullname number must be set")
        if not phone:
            raise ValueError("The phone number must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)

        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("The superuser is_staff must be True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("The superuser is_superuser must be True")
        if extra_fields.get("is_active") is not True:
            raise ValueError("The superuser is_active must be True")
        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(
        max_length=30,
    )
    last_name = models.CharField(
        max_length=30,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    EXTRA_FIELS = [first_name, last_name]

    def __str__(self):
        return self.phone


class PasswordResetOTP(models.Model):
    phone = models.CharField(max_length=11)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp_code = str(random.randint(100000,999999))
        self.created_at = timezone.now()
        self.is_used = False
        self.save()
        return self.otp_code