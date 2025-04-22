from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_unit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_units')

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = [
        ('basic', 'Basic'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='basic')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)

class LoginRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.timestamp}"


    def __str__(self):
        return f"{self.username} ({self.role})"
