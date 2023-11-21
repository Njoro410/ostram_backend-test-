from django.db import models
from administration.choices import *
from django.conf import settings
# Create your models here.


class ResidentialAreas(models.Model):
    area_code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=22, decimal_places=6, blank=True, null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="residentialArea_instance_creator",
        blank=True,
        null=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        related_name="residentialArea_instance_updater",
        null=True,
    )

    class Meta:
        db_table = "residential_areas"

    def __str__(self):
        return self.name


class Members(models.Model):
    names = models.CharField(max_length=255, null=True, blank=True)
    mbr_no = models.IntegerField(primary_key=True)
    id_no = models.CharField(blank=True, null=True, max_length=50)
    gender = models.CharField(
        null=True, blank=True, max_length=255, choices=GENDER_CHOICES
    )
    residential = models.ForeignKey(
        ResidentialAreas, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    phone_no = models.CharField(blank=True, null=True, max_length=255)
    next_of_kin = models.CharField(max_length=255, null=True, blank=True)
    phone_nos = models.CharField(blank=True, null=True, max_length=255)
    relationship = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        upload_to="members/passport_photo/", blank=True, null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    kra_pin = models.CharField(blank=True, null=True, max_length=60)



    def __str__(self):
        return self.names

    class Meta:
        db_table = "members"
        ordering = ["mbr_no"]
