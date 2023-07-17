from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
import datetime


class AccessTokenManager(models.Manager):
    def get_first_token(self):
        return self.first()


class AccessToken(models.Model):
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    objects = AccessTokenManager()

    def __str__(self):
        return self.token

    def is_expired(self):
        now = timezone.now()
        return self.expires_at <= now


@receiver(pre_save, sender=AccessToken)
def set_expires_at(sender, instance, **kwargs):
    if not instance.expires_at:
        instance.expires_at = timezone.now() + timedelta(minutes=50)
    else:
        # Update the expires_at field if the token is being updated
        original_token = sender.objects.filter(
            pk=instance.pk).values('token').first()
        if instance.token != original_token['token']:
            instance.expires_at = timezone.now() + timedelta(minutes=50)


class LipaNaMpesaCallback(models.Model):
    merchant_request_id = models.CharField(max_length=255)
    checkout_request_id = models.CharField(max_length=255)
    result_code = models.IntegerField()
    result_desc = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=255)
    transaction_date = models.DateTimeField()
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.merchant_request_id


class Transaction(models.Model):
    transaction_type = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    transaction_time = models.CharField(max_length=100)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    business_short_code = models.CharField(max_length=100)
    bill_ref_number = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100)
    org_account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    third_party_trans_id = models.CharField(max_length=100)
    msisdn = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{first_name} {last_name}'s transaction"
