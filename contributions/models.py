from django.db import models
from django.conf import settings
from members.models import Members
# Create your models here.

class DailyContributions(models.Model):
    account_no = models.ForeignKey(
        Members, on_delete=models.CASCADE, related_name='daily_contributions')
    savings = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    deposits = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_repayment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_interest = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    maintenance_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    general_charges = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    late_charges = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_processing = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    affidavit_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='daily_contirbutions_recipient', blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='daily_contributions_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = "daily_contributions"
        ordering = ["-received_date"]

    def __str__(self):
        return f"{self.account_no.names}'s {self.received_date}"