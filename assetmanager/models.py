from django.db import models
from administration.choices import *
from administration.models import baseModel
from members.models import members
from administration.models import Branch

# Create your models here.


class Asset(baseModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    expiry_date = models.DateField(null=True)
    inspection_date = models.DateField(null=True)
    owner = models.ForeignKey(members, on_delete=models.CASCADE,)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    value = models.IntegerField(null=True)

    class Meta:
        db_table = "asset"

    def __str__(self):
    	return self.name
 
class officeAsset(Asset):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True,blank=True)
    class Meta:
         db_table = "office_asset"
         
    def __str__(self):
        return f"{branch.location.name}'s office asset"
 




class assetDocument(baseModel):
    upload_date = models.DateField(auto_now_add=True)
    document_name = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(upload_to='assetdocuments/')
    proof_of = models.ForeignKey(Asset, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "asset_document"
        
    def __str__(self):
        return self.document_name
    
		
	