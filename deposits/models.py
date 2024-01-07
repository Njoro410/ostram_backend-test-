from django.db import models
from members.models import Members
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.db import transaction
# Create your models here.

@receiver(post_save, sender=Members)
def create_savings_account(sender,instance,created,**kwargs):
    if created:
        DepositsAccount.objects.create(
            account_owner=instance,
            deposits_balance=0,
            created_on=date.today(),
            updated_on=date.today(),
            created_by=instance.created_by,
            updated_by=instance.created_by,  
        )

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
        return f"{self.account_owner.names}  {self.deposits_balance}"


        
class ReceiveDeposits(models.Model):
    account = models.ForeignKey(DepositsAccount, on_delete=models.CASCADE, related_name="depositsplus")
    received_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    received_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='depositsplus_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='depositsplus_instance_updater', null=True)
    
    def __str__(self):
        return f"{self.account.account_owner.names}'s {self.received_date}"
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update the balance of this member's deposits account by adding received amount
        self.account.deposits_balance += self.received_amount
        self.account.save()

        
class WithdrawDeposits(models.Model):
    account = models.ForeignKey(DepositsAccount, on_delete=models.CASCADE, related_name="depositsminus")
    withdrawn_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    withdrawn_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='depositsminus_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='depositsminus_instance_updater', null=True)
    
    def __str__(self):
        return f"{self.account.account_owner.names}'s {self.withdrawn_date}"
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update the balance of this member's deposits account by reducing received amount
        self.account.deposits_balance -= self.withdrawn_amount
        self.account.save()