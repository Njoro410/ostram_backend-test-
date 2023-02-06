from django.db import models

# Create your models here.

class Residential_Areas(models.Model):
  area_code = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=120)


  def __str__(self):
      return self.name

class Members(models.Model):
  names = models.CharField(max_length=120, null = True, blank=True)
  mbr_no = models.IntegerField()
  id_no = models.IntegerField(blank=True, null=True)
  gender = models.CharField(null = True, blank=True, max_length=120)
  residential = models.ForeignKey(Residential_Areas, on_delete=models.DO_NOTHING, null=True, blank=True)
  phone_no = models.CharField(blank=True, null=True, max_length=120)
  next_of_kin = models.CharField(max_length=120, null=True, blank=True)
  phone_nos = models.CharField(blank=True, null=True, max_length=120)
  relationship = models.CharField(max_length=120, null = True, blank=True)
  kra_pin = models.CharField(blank=True, null=True, max_length=60)

  def __str__(self):
      return self.names


