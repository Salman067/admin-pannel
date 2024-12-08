from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    user_type = models.CharField(max_length=255, default='admin')
    username = None  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

