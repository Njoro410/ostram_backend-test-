from django.contrib import admin
from .models import SavingsAccount,ReceiveSavings,WithdrawSavings
# Register your models here.
admin.site.register(SavingsAccount)
admin.site.register(ReceiveSavings)
admin.site.register(WithdrawSavings)