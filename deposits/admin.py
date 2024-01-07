from django.contrib import admin
from .models import DepositsAccount, ReceiveDeposits, WithdrawDeposits
# Register your models here.
admin.site.register(DepositsAccount)
admin.site.register(ReceiveDeposits)
admin.site.register(WithdrawDeposits)