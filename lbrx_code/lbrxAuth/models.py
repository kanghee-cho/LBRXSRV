from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class LbrxUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="lbrxuser_set",  # Custom related_name to avoid clashes
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="lbrxuser_set",  # Custom related_name to avoid clashes
        blank=True,
    )

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.username}({self.email})"