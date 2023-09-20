from django.db import models
from members.models import ResidentialAreas, Members
from django.contrib.auth.models import User
from .choices import *
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from .choices import BRANCH_STATUS_CHOICES

# Create your models here.


# class baseModel(models.Model):
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='instance_creator', blank=True, null=True)
#     created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
#     updated_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='instance_updater', null=True)

#     class Meta:
#         db_table = "base_model"

class BranchStatus(models.Model):
    name = models.CharField(max_length=200, choices=BRANCH_STATUS_CHOICES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='branch_status_creator', null=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='branch_status_updater', null=True)

    class Meta:
        db_table = "branch_status"

    def __str__(self):
        return self.name


class Branch(models.Model):
    full_address = models.CharField(max_length=200, null=True, blank=True)
    location = models.ForeignKey(ResidentialAreas, on_delete=models.PROTECT)
    phone = models.CharField(blank=True, null=True, max_length=15)
    email = models.EmailField(null=True, blank=True)
    status = models.ForeignKey(
        BranchStatus, on_delete=models.PROTECT, blank=True, null=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='branch_manager')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='created_by_on_branch')
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='updated_by_branch', null=True)

    class Meta:
        db_table = "branch"

    def __str__(self):
        return self.location.name


# class Staff(baseModel):
#     user = models.OneToOneField(
#         User, on_delete=models.PROTECT, related_name='staff')
#     title = models.CharField(max_length=200, blank=True, choices=TITLE_CHOICES)
#     fullname = models.CharField(max_length=200, blank=True)
#     phone_number = PhoneNumberField(blank=True)
#     gender = models.CharField(
#         max_length=200, choices=GENDER_CHOICES, blank=True)
#     dob = models.DateField(blank=True, null=True)
#     current_salary = models.IntegerField(blank=True)
#     employment_date = models.DateField(blank=True, null=True)
#     years_in_workplace = models.IntegerField(blank=True)
#     marital_status = models.CharField(
#         max_length=200, choices=RELATIONSHIP_STATUS_CHOICES, blank=True)
#     picture = models.ImageField(
#         max_length=200, blank=True, upload_to='employee/')
#     educational_status = models.CharField(
#         max_length=200, choices=EDUCATIONAL_STATUS_CHOICES, blank=True)
#     manager = models.ForeignKey(
#         User, on_delete=models.PROTECT, related_name='manager', blank=True, null=True)

#     class Meta:
#         db_table = "staff"

#     def __str__(self):
#         return self.fullname


class globalCharges(models.Model):
    member = models.ForeignKey(
        Members, on_delete=models.PROTECT, null=True, blank=True)
    maintenance_fee = models.DecimalField(max_digits=10, decimal_places=2)
    general_charges = models.DecimalField(max_digits=10, decimal_places=2)
    affidavit_fee = models.DecimalField(max_digits=10, decimal_places=2)
    passbook = models.DecimalField(max_digits=10, decimal_places=2)
    registration_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='globalCharges_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='globalCharges_instance_updater', null=True)

    class Meta:
        db_table = "global_charges"

    def __str__(self):
        return self.member.names
