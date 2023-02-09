from django.db import models
from members.models import members
from administration.choices import *
from administration.models import baseModel
# from assetmanager.models import Asset

# Create your models here.


class Loan_Type(models.Model):
    name = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=5, decimal_places=5)
    description = models.TextField()
    need_collateral = models.BooleanField(
        help_text='does this type of Loan need Coollateral')
    need_guarantor = models.BooleanField(
        help_text='does this type of loan need a gurantor')
    documents = models.ManyToManyField(
        'documentType', help_text="Include documents that are needed here for this particular loan.. You can go to the document section to add or delete document")
    min_amount_allowed = models.IntegerField(
        null=True, blank=True)
    max_amount_allowed = models.IntegerField(null=True, blank=True)
    processing_fee = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    insurance_fee = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    
    class Meta:
        db_table = "loan_type"
    

    def __str__(self):
        return self.name


class Loans(models.Model):
    lendee = models.ForeignKey(
        members, on_delete=models.DO_NOTHING, related_name='borrower')
    loan_type = models.ForeignKey(Loan_Type, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
    application_date = models.DateField(auto_now_add=False)
    issue_date = models.DateField(auto_now_add=False)
    repayment_date = models.DateField(auto_now_add=False)
    guarantors = models.ManyToManyField(members, related_name='guarantors')
    payment_frequency = models.CharField(
        max_length=50, choices=PAYMENT_FREQUENCY_CHOICES)
    repaid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    # collateral = models.ForeignKey(
    #     Asset, on_delete=models.CASCADE, related_name='loan_colateral', null=True, blank=True)

    
    class Meta:
        db_table = "loans"
        
    def __str__(self):
        return f"{self.lendee.names}'s loan"

    @property
    def borrower_membership_number(self):
        return self.lendee.mbr_no




class Documents(baseModel):
    upload_date = models.DateField(auto_now_add=True)
    loan = models.ForeignKey(
        Loans, on_delete=models.CASCADE, null=True, related_name='loan_documents')
    document_type = models.ForeignKey(
        'documentType', on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='documents/')
    
    class Meta:
        db_table = "documents"

    def __str__(self):
        return f" {self.document_type.name}"


class documentType(baseModel):
    name = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    description = models.TextField()
    
    class Meta:
        db_table = "document_type"

    def __str__(self):
        return self.name
