from django.db import models
from members.models import Members
from django.conf import settings
# Create your models here.
class DepositsAccount(models.Model):
    account_owner = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='deposits_account')  
    deposits_balance = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='deposits_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='deposits_instance_updater', null=True)
    
    class Meta:
        db_table = "deposits_account"
    
    def __str__(self):
        return self.account_owner.names
    