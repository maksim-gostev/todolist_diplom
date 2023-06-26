from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'


class User(AbstractUser):
    REQUIRED_FIELDS = []
    phone = models.CharField(max_length=12)
    role = models.CharField(max_length=5, choices=UserRole.choices, default=UserRole.USER)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
