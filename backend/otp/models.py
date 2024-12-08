from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, validate_email
import datetime

phone_regex = RegexValidator(
    regex=r"^\d{11}", message="Phone number must be 11 digits only."
)

class UserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None):
        if not phone_number:
            raise ValueError("Phone number is required")
        
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email=None, password=None):
        user = self.create_user(phone_number=phone_number, email=email, password=password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserModel(AbstractUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True, validators=[phone_regex], null=False, blank=False)
    email = models.EmailField(max_length=50, validators=[validate_email], null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_regitered_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = "phone_number"
    
    objects = UserManager()
    
    def __str__(self):
        return self.phone_number
