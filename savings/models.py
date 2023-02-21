from django.db import models
from members.models import members
from administration.models import baseModel

# Create your models here.
class Savings_Account(baseModel):
    account_owner = models.ForeignKey(members, on_delete=models.CASCADE, related_name='savings_account')  
    balance = models.DecimalField(max_digits=8, decimal_places=3)
    
    class Meta:
        db_table = "savings_account"
    
    def __str__(self):
        return self.account_owner.names
    