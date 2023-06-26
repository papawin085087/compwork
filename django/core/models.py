"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.conf import settings


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255, blank=True)
    employee_type = models.CharField(max_length=255, blank=True)
    team = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Task(models.Model):
    """Task object. """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(blank=True, null=True, auto_now=True)
    time_start = models.TimeField(auto_now_add=True)
    time_end = models.TimeField(blank=True, null=True, auto_now=True)
    task_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class EventType(models.Model):

    event_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.event_type


class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    event_title = models.CharField(max_length=255, blank=True, default='sick')
    event_description = models.TextField(blank=True)
    event_status = models.BooleanField(default=False, blank=True, null=True)
    event_type = models.ForeignKey(
        EventType, on_delete=models.CASCADE, blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    event_end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.event_title


class CheckIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    check_status = models.BooleanField(default=True, blank=True, null=True)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(auto_now=True)
