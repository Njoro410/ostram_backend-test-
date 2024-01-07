from django.db import models
from django.conf import settings
from members.models import Members
# Create your models here.


class DailyContributions(models.Model):
    member = models.ForeignKey(
        Members, on_delete=models.CASCADE, related_name='daily_contributions')
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    collection_date = models.DateField(blank=True, null=True)
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='daily_contirbutions_recipient', blank=True, null=True)
    savings = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    deposits = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_interest = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_repayment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    maintenance_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    late_charges = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    registration_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_processing_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_insurance_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    affidavit_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    loan_form = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    passbook = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    general_charges = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='daily_contributions_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = "daily_contributions"
        ordering = ['-collection_date']

    def __str__(self):
        return f"{self.member.names}'s {self.collection_date}"

    @classmethod
    def get_or_create_daily_contributions(cls, member, collection_date, savings,total_amount):
        daily_contributions, created = cls.objects.get_or_create(
            member=member,
            collection_date=collection_date,
            total_amount=total_amount,
            savings=savings,
            # defaults={
            #     # assuming you have a created_by field in your Members model
            #     'received_by': member.created_by,
            #     # ... other default values ...
            # }
        )
        return daily_contributions
