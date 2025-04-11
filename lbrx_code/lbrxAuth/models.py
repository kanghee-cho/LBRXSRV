from django.db import models
from django.contrib.auth.models import AbstractUser

class LbrxUser(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=False)
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return f"{self.nickname}({self.email})"