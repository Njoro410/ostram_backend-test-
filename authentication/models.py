from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from administration.choices import *
from phonenumber_field.modelfields import PhoneNumberField
from .managers import AccountManager
from django.conf import settings
from administration.models import Branch
import uuid

# Create your models here.


class staffAccount(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    otp_base32 =  models.CharField(max_length = 200, null = True)
    username = models.CharField(max_length=50, blank=False, null=False)
    is_admin = models.BooleanField(default=False, blank=False, null=False)
    is_active = models.BooleanField(
        default=True, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.", blank=False, null=False)
    is_staff = models.BooleanField(
        default=False, help_text="Designates whether the user can log into this admin site.", blank=False, null=False)
    is_superuser = models.BooleanField(
        default=False, help_text="Designates that this user has all permissions without explicitly assigning them.", blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, blank=True,
                             null=True, choices=TITLE_CHOICES)
    role = models.CharField(max_length=200, blank=True,
                            null=True, choices=ROLES)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(
        max_length=200, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    current_salary = models.IntegerField(blank=True, null=True)
    reports_to = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, related_name='manager', blank=True, null=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=True, null=True)
    is_authenticator = models.BooleanField(default=False)
    logged_in = models.BooleanField(default = False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    # GRANT ALL PERMISSIONS TO EVERYONE (NOT RECOMMENDED)
    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True
