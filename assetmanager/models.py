from django.db import models
from administration.choices import *
from authentication.models import baseModel
from members.models import members
from loans.models import Loans
# from administration.models import Branch
from django.conf import settings


# Create your models here.


class loanAsset(models.Model):
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    expiry_date = models.DateField(null=True,blank=True)
    inspection_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    value = models.IntegerField(null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='loanAsset_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='loanAsset_instance_updater', null=True)

    class Meta:
        db_table = "loan_asset"

    def __str__(self):
    	return f"{self.loan.lendee.names}'s {self.name}"
 


class assetDocument(models.Model):
    upload_date = models.DateField(auto_now_add=True)
    document_name = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(upload_to='assetdocuments/',null=True)
    proof_of = models.ForeignKey(loanAsset, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='assetDocument_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='assetDocument_instance_updater', null=True)
    
    class Meta:
        db_table = "asset_document"
        
    def __str__(self):
        return self.document_name
    
		
	
