from django.db import models
from members.models import Members
from administration.models import baseModel

# Create your models here.
class Savings_Account(baseModel):
    account_owner = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='savings_account')  
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    
    
    def __str__(self):
        return self.account_owner.names
    