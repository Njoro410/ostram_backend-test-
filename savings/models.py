from django.db import models
from django.conf import settings
from members.models import Members
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.db import transaction

@receiver(post_save, sender=Members)
def create_savings_account(sender,instance,created,**kwargs):
    if created:
        SavingsAccount.objects.create(
            account_owner=instance,
            savings_balance=0,
            created_on=date.today(),
            updated_on=date.today(),
            created_by=instance.created_by,
            updated_by=instance.created_by,  
        )

class SavingsAccount(models.Model):
    account_owner = models.ForeignKey(
        Members, on_delete=models.CASCADE, related_name='savings_account')
    savings_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='savings_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='savings_instance_updater', null=True)

    class Meta:
        db_table = "savings_account"

    def __str__(self):
        return f"{self.account_owner.names}'s Saving Account"
    
class ReceiveSavings(models.Model):
    account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name="savingsplus")
    received_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    received_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='savingsplus_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='savingsplus_instance_updater', null=True)
    
    def __str__(self):
        return f"{self.account.account_owner.names}'s {self.received_date}"
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update the balance of this member's saving account by adding received amount
        self.account.savings_balance += self.received_amount
        self.account.save()

        
class WidthdrawSavings(models.Model):
    account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name="savingsminus")
    received_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    received_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='savingsminus_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='savingsminus_instance_updater', null=True)
    
    def __str__(self):
        return f"{self.account.account_owner.names}'s {self.received_date}"
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update the balance of this member's saving account by reducing received amount
        self.account.savings_balance -= self.received_amount
        self.account.save()

