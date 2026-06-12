from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_SUPERADMIN = 'superadmin'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_SUPERADMIN, 'Superadmin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_ADMIN)

    class Meta:
        db_table = 'users'

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
