from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from administration.choices import *
from phonenumber_field.modelfields import PhoneNumberField
from .managers import AccountManager
# Create your models here.

class staffAccount(AbstractBaseUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    username = models.CharField(max_length=50, blank=False, null=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, blank=True,
                             null=True, choices=TITLE_CHOICES)
    role = models.CharField(max_length=200, blank=True,
                             null=True, choices=ROLES)
    fullname = models.CharField(max_length=200, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(
        max_length=200, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    current_salary = models.IntegerField(blank=True, null=True)
    reports_to = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, related_name='manager', blank=True, null=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
