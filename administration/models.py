from django.db import models
from members.models import residential_areas
from django.contrib.auth.models import User
from .choices import *
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class baseModel(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applicationcreator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name='applicationupdater', null=True)
    branch = models.ForeignKey(
        'Branch', on_delete=models.CASCADE, default=1, null=True)

    def audit(self, request):
        self.created_by = request.user
        self.branch = request.user.person.branch

    class Meta:
        db_table = "base_model"


class Branch(models.Model):
    full_address = models.CharField(max_length=200, null=True, blank=True)
    location = models.ForeignKey(residential_areas, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name='branch_manager')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name='created_by_on_branch')
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name='updated_by_branch')
    
    
    class Meta:
        db_table = "branch"

    def __str__(self):
        return self.location.name


class Staff(baseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='staff')
    title = models.CharField(max_length=200, blank=True, choices=TITLE_CHOICES)
    fullname = models.CharField(max_length=200, blank=True)
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(
        max_length=200, choices=GENDER_CHOICES, blank=True)
    dob = models.DateField(blank=True, null=True)
    current_salary = models.IntegerField(blank=True)
    employment_date = models.DateField(blank=True, null=True)
    years_in_workplace = models.IntegerField(blank=True)
    marital_status = models.CharField(
        max_length=200, choices=RELATIONSHIP_STATUS_CHOICES, blank=True)
    picture = models.ImageField(
        max_length=200, blank=True, upload_to='employee/')
    educational_status = models.CharField(
        max_length=200, choices=EDUCATIONAL_STATUS_CHOICES, blank=True)
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='manager', blank=True, null=True)
    
    class Meta:
        db_table = "staff"

    def __str__(self):
        return self.fullname


class globalCharges(models.Model):
    name = models.CharField(max_length=50)
    maintenance_fee = models.DecimalField(max_digits=5, decimal_places=2)
    late_charges = models.DecimalField(max_digits=5, decimal_places=2)
    loan_form = models.DecimalField(max_digits=5, decimal_places=2)
    general_charges = models.DecimalField(max_digits=5, decimal_places=2)
    affidavit_fee = models.DecimalField(max_digits=5, decimal_places=2)
    passbook = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        db_table = "global_charges"
    
    def __str__(self):
        return self.name
    