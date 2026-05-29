from django.db import models
from django.contrib.auth.models import AbstractUser

class Division(models.Model):
    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    division = models.ForeignKey(Division, null=True, blank=True, on_delete=models.SET_NULL)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(max_length=50, default='user')
    is_active = models.BooleanField(default=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
